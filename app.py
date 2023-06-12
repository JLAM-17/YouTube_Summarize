from flask import Flask, jsonify, request
from youtube_api import extract_video_id,get_captions, get_video_details
from flask_cors import CORS



app = Flask(__name__, static_folder='frontend/build', static_url_path='/')
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})




@app.route('/api/summarize', methods=['POST'])
def summarize():
    video_link = request.json['videoLink']
    # Extract the video ID from the YouTube video link
    video_id = extract_video_id(video_link)
    # Get the video details
    video_details = get_video_details(video_id)
    # Get the video captions
    print(video_details)
    captions = get_captions(video_id,video_details["defaultLanguage"][:2])
    print(captions)
    return jsonify({'captions': captions})


@app.route('/api')
def api():
    return jsonify({'message': 'Hello from Flask API!'})

@app.route('/')
def serve_frontend():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)
