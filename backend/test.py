import praw
import os
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe" #delete this line if not windows
from gtts import gTTS
from moviepy.editor import ColorClip, AudioFileClip, TextClip, CompositeVideoClip
import textwrap

# Reddit API setup
reddit = praw.Reddit(
    client_id="Yl764s-6k88VD35HH_0Blg",
    client_secret="ERcLaAGDDypF0OQolfKcF9_aPlS0iA",
    user_agent="test by u/Silly_Inspection5308"
)

def create_text_clips(text, audio_duration, fontsize=40, color='white'):
    # Split text into sentences and clean them
    sentences = [s.strip() for s in text.replace('\n', ' ').split('.') if s.strip()]
    clips = []
    current_time = 0
    
    # Calculate total words
    total_words = sum(len(sentence.split()) for sentence in sentences)
    words_per_second = total_words / audio_duration
    
    for sentence in sentences:
        # Calculate duration based on word count
        word_count = len(sentence.split())
        duration = word_count / words_per_second
        
        # Wrap text to fit screen width (approximately 60 characters per line)
        wrapped_text = textwrap.fill(sentence + '.', width=60)
        
        # Create a clip for each sentence
        clip = TextClip(wrapped_text, fontsize=fontsize, color=color, font='Arial', method='caption', size=(1000, None))
        clip = clip.set_position(('center', 'center')).set_start(current_time).set_duration(duration)
        clips.append(clip)
        current_time += duration
    
    return clips

def create_video(submission_title, submission_text):
    # Create a temporary directory for our assets
    if not os.path.exists('temp'):
        os.makedirs('temp')
    
    # Generate audio from text with different voice
    # Available options for English:
    # 'en' - US English
    # 'en-uk' - British English
    # 'en-au' - Australian English
    # 'en-ca' - Canadian English
    # 'en-in' - Indian English
    tts = gTTS(text=submission_text, lang='en-uk', slow=False)
    tts.save('temp/audio.mp3')
    
    # Load the audio
    audio = AudioFileClip('temp/audio.mp3')
    audio_duration = audio.duration
    
    # Create a black background video
    background = ColorClip(size=(1080, 1920), color=(0, 0, 0))
    background = background.set_duration(audio_duration)
    
    # Create title clip with wrapping and fade effects
    wrapped_title = textwrap.fill(submission_title, width=40)
    title_clip = TextClip(wrapped_title, fontsize=30, color='white', font='Arial-Bold', method='caption', size=(1000, None))
    title_clip = title_clip.set_position(('center', 100))
    # Make title appear for first 3 seconds with fade in/out
    title_clip = title_clip.set_duration(3).crossfadein(0.5).crossfadeout(0.5)
    
    # Create text clips synchronized with audio
    text_clips = create_text_clips(submission_text, audio_duration)
    
    # Create a frame around the text
    frame_width = 1060  # Slightly smaller than video width
    frame_height = 1800  # Slightly smaller than video height
    frame = ColorClip(size=(frame_width, frame_height), color=(50, 50, 50))  # Dark gray frame
    frame = frame.set_position(('center', 'center')).set_duration(audio_duration)
    
    # Create a slightly smaller black background for the text
    text_bg = ColorClip(size=(1040, 1780), color=(0, 0, 0))
    text_bg = text_bg.set_position(('center', 'center')).set_duration(audio_duration)
    
    # Combine all elements
    final_video = CompositeVideoClip([
        background,
        frame,
        text_bg,
        title_clip
    ] + text_clips)
    final_video = final_video.set_audio(audio)
    
    # Write the result to a file
    final_video.write_videofile('output.mp4', fps=24)
    
    # Clean up temporary files
    for file in ['temp/audio.mp3']:
        if os.path.exists(file):
            os.remove(file)

# Get the Reddit submission
#submission = reddit.submission(url="https://www.reddit.com/r/AITAH/comments/1kukjww/aita_for_not_telling_my_sister_the_name_chosen/")
submission = reddit.submission(url="https://www.reddit.com/r/AITAH/comments/1ktt8cq/aita_for_dumping_my_boyfriend_for_saying_a_womans/")
submission_text = submission.selftext
submission_title = submission.title

# Create the video
create_video(submission_title, submission_text)

