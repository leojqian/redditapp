from flask import Flask, request, jsonify
from flask_cors import CORS
import praw
import os
from gtts import gTTS
from moviepy.editor import ColorClip, AudioFileClip, TextClip, CompositeVideoClip
import textwrap

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Reddit API setup
reddit = praw.Reddit(
    client_id="Yl764s-6k88VD35HH_0Blg",
    client_secret="ERcLaAGDDypF0OQolfKcF9_aPlS0iA",
    user_agent="test by u/Silly_Inspection5308"
)

def create_text_clips(text, audio_duration, fontsize=40, color='white'):
    sentences = [s.strip() for s in text.replace('\n', ' ').split('.') if s.strip()]
    clips = []
    current_time = 0
    
    total_words = sum(len(sentence.split()) for sentence in sentences)
    words_per_second = total_words / audio_duration
    
    for sentence in sentences:
        word_count = len(sentence.split())
        duration = word_count / words_per_second
        
        wrapped_text = textwrap.fill(sentence + '.', width=60)
        
        clip = TextClip(wrapped_text, fontsize=fontsize, color=color, font='Arial', method='caption', size=(1000, None))
        clip = clip.set_position(('center', 'center')).set_start(current_time).set_duration(duration)
        clips.append(clip)
        current_time += duration
    
    return clips

def create_video(submission_title, submission_text):
    if not os.path.exists('temp'):
        os.makedirs('temp')
    
    tts = gTTS(text=submission_text, lang='en', slow=False)
    tts.save('temp/audio.mp3')
    
    audio = AudioFileClip('temp/audio.mp3')
    audio_duration = audio.duration
    
    background = ColorClip(size=(1080, 1920), color=(0, 0, 0))
    background = background.set_duration(audio_duration)
    
    wrapped_title = textwrap.fill(submission_title, width=40)
    title_clip = TextClip(wrapped_title, fontsize=30, color='white', font='Arial-Bold', method='caption', size=(1000, None))
    title_clip = title_clip.set_position(('center', 100))
    title_clip = title_clip.set_duration(3).crossfadein(0.5).crossfadeout(0.5)
    
    text_clips = create_text_clips(submission_text, audio_duration)
    
    frame_width = 1060
    frame_height = 1800
    frame = ColorClip(size=(frame_width, frame_height), color=(50, 50, 50))
    frame = frame.set_position(('center', 'center')).set_duration(audio_duration)
    
    text_bg = ColorClip(size=(1040, 1780), color=(0, 0, 0))
    text_bg = text_bg.set_position(('center', 'center')).set_duration(audio_duration)
    
    final_video = CompositeVideoClip([
        background,
        frame,
        text_bg,
        title_clip
    ] + text_clips)
    final_video = final_video.set_audio(audio)
    
    output_path = 'temp/output.mp4'
    final_video.write_videofile(output_path, fps=24)
    
    return output_path

@app.route('/api/create-video', methods=['POST'])
def create_video_endpoint():
    try:
        data = request.json
        reddit_url = data.get('redditUrl')
        
        if not reddit_url:
            return jsonify({'error': 'Reddit URL is required'}), 400
        
        submission = reddit.submission(url=reddit_url)
        video_path = create_video(submission.title, submission.selftext)
        
        return jsonify({
            'success': True,
            'videoPath': video_path,
            'title': submission.title,
            'text': submission.selftext
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 