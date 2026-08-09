import os
import subprocess
from pytube import YouTube

def download_audio(youtube_url, output_folder="downloads"):
    os.makedirs(output_folder, exist_ok=True)
    yt = YouTube(youtube_url)
    print(f"Downloading audio from: {yt.title}")
    audio_stream = yt.streams.filter(only_audio=True).first()
    file_path = audio_stream.download(output_path=output_folder)
    return yt.title, file_path

def audio_to_video(audio_file, image_file, output_file="output.mp4"):
    if not os.path.exists(audio_file):
        raise FileNotFoundError(f"Audio file not found: {audio_file}")
    if not os.path.exists(image_file):
        raise FileNotFoundError(f"Image file not found: {image_file}")

    command = [
        "ffmpeg", "-loop", "1",
        "-i", image_file,
        "-i", audio_file,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        output_file
    ]

    subprocess.run(command, check=True)
    print(f"Video created: {output_file}")

if __name__ == "__main__":
    yt_url = input("Enter YouTube video URL: ")
    thumbnail_path = input("Enter thumbnail image path (JPG/PNG): ")
    output_video = input("Enter output video file name (e.g., video.mp4): ")

    title, audio_path = download_audio(yt_url)
    audio_to_video(audio_path, thumbnail_path, output_video)
