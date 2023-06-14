from flask import Flask, jsonify, request
from flask_cors import CORS
from youtube_api import extract_video_id,get_captions, get_video_details
from db import insert_video, get_video_by_id
from openai_api import video_summarize


# app = Flask(__name__)
app = Flask(__name__, static_folder='frontend/build', static_url_path='/')
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

@app.route('/api/summarize', methods=['POST'])
def summarize():
    video_link = request.json['videoLink']
    # Extract the video ID from the YouTube video link
    try:
        video_id = extract_video_id(video_link)
    except:
        return jsonify({'error': 'Invalid video link'}), 404
    # Get the video details
    try:
        video_details = get_video_details(video_id)
    except:
        return jsonify({'error': 'Video not found'}), 404
    # Get the video captions
    try:
        captions = get_captions(video_id,video_details["defaultLanguage"][:2])
        transcript = ' '.join([caption['text'] for caption in captions])
    except:
        return jsonify({'error': 'Captions not found'}), 404
    # Summarize the captions
    try:
        summary = video_summarize(transcript, video_details)
    except:
        return jsonify({'error': 'Video is too large to be processed'}), 413
    # Insert the video into the database
    try:
        video_id = insert_video(video_details, summary)
    except:
        return jsonify({'error': 'Video could not be inserted into the database'}), 500
    return jsonify({'video_id':video_id })

@app.route('/api/video/<video_id>', methods=['GET'])
def get_video(video_id):
    # Retrieve the video from the database
    video = get_video_by_id(video_id)
    if video is None:
        return jsonify({'error': 'Video not found'})
    return jsonify(video)

@app.route('/api')
def api():
    return jsonify({'message': 'Hello from Flask API!'})

@app.route('/')
def serve_frontend():
    return app.send_static_file('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)
