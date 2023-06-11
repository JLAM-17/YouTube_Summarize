from flask import Flask, jsonify

app = Flask(__name__, static_folder='frontend/build', static_url_path='/')

@app.route('/api')
def api():
    return jsonify({'message': 'Hello from Flask API!'})

@app.route('/')
def serve_frontend():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)
