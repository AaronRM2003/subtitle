import os
import time
import yt_dlp
import assemblyai as aai

# Set your AssemblyAI API key here directly or via environment variable
aai.settings.api_key = "91ed4cffb8a54c9cba735a07447472c2"
# Alternatively, to use environment variable:
# aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

def download_audio_from_youtube(url, output_format="mp3"):
    ydl_opts = {
        "format": "bestaudio/best",
        "extractaudio": True,
        "audioquality": 1,
        "outtmpl": "downloaded_audio.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": output_format,
            "preferredquality": "192",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
        # Replace original extension with output format extension
        return filename.rsplit('.', 1)[0] + f'.{output_format}'

def transcribe_audio(file_path):
    transcriber = aai.Transcriber()
    print(f"Uploading and transcribing '{file_path}' ...")
    transcript = transcriber.transcribe(file_path)

    while transcript.status not in ("completed", "error"):
        print(f"Status: {transcript.status}. Waiting 10 seconds...")
        time.sleep(10)
        transcript = transcriber.get(transcript.id)

    if transcript.status == "error":
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    print("Transcription completed.")
    return transcript.text

def main():
    video_url = input("Enter the YouTube video URL: ").strip()
    audio_file = download_audio_from_youtube(video_url)
    print(f"Downloaded and converted audio to: {audio_file}")

    transcript_text = transcribe_audio(audio_file)

    print("\nFull Transcript:\n")
    print(transcript_text)

    with open("transcript.txt", "w", encoding="utf-8") as f:
        f.write(transcript_text)
    print("\nTranscript saved to 'transcript.txt'.")

if __name__ == "__main__":
    main()
