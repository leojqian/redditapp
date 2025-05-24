from pytube import YouTube

url = "https://youtu.be/u7kdVe8q5zs?si=CGViexwatGOWhyYu"
yt = YouTube(url)

stream = yt.streams.get_highest_resolution()  # or get_by_itag(), get_audio_only()
stream.download(output_path="/Users/yourusername/Downloads", filename="minecraft_clip.mp4")