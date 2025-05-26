from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from threading import Thread
import uuid
import os
from test import generate_video_from_reddit

app = Flask(__name__)
CORS(app)

# Store job statuses and paths
jobs = {}  # job_id → { status: 'pending' | 'done', path: '...' }

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    reddit_url = data.get('reddit_url')

    if not reddit_url:
        return jsonify({ 'error': 'Missing reddit_url' }), 400

    # Generate unique job ID and output path
    job_id = str(uuid.uuid4())
    output_path = f'temp/{job_id}.mp4'
    jobs[job_id] = { 'status': 'pending', 'path': output_path }

    # Define and start background job
    def worker():
        try:
            generate_video_from_reddit(reddit_url, output_path)
            jobs[job_id]['status'] = 'done'
        except Exception as e:
            jobs[job_id]['status'] = f'error: {str(e)}'

    Thread(target=worker).start()

    return jsonify({ 'job_id': job_id }), 202

@app.route('/status/<job_id>', methods=['GET'])
def status(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({ 'error': 'Job not found' }), 404
    return jsonify({ 'status': job['status'] })

@app.route('/video/<job_id>', methods=['GET'])
def video(job_id):
    job = jobs.get(job_id)
    if not job or job['status'] != 'done':
        return jsonify({ 'error': 'Video not ready' }), 404
    return send_file(job['path'], mimetype='video/mp4', as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists('temp'):
        os.makedirs('temp')
    app.run(debug=True)
