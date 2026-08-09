import assemblyai as aai
from pathlib import Path
import yt_dlp
import os

# 🔑 Set your API key
aai.settings.api_key = "91ed4cffb8a54c9cba735a07447472c2"

def download_youtube_audio(yt_url, output_path="yt_audio.mp3"):
    """Downloads the best quality audio from a YouTube URL and converts to MP3."""
    print(f"Downloading audio from: {yt_url}")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        # yt-dlp automatically appends the extension, so we strip it from the output template
        'outtmpl': output_path.replace('.mp3', ''),
        'quiet': False,
        'no_warnings': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_url])
        print(f"Successfully downloaded to: {output_path}")
        return output_path
    except Exception as e:
        print(f"Failed to download YouTube video: {e}")
        return None

def transcribe_word_level_srt(audio_file, output_file="word_level.srt", language_code="ml"):
    """Transcribes an audio file and generates a word-level SRT."""
    print(f"Uploading and transcribing {audio_file}...")
    
    transcriber = aai.Transcriber()
    # Explicitly set the language code so AssemblyAI knows what to expect
    config = aai.TranscriptionConfig(language_code=language_code)
    
    transcript = transcriber.transcribe(audio_file, config=config)

    if transcript.status != "completed":
        print("Transcription failed:", transcript.error)
        return

    words = transcript.words

    if not words:
        print("No words were found in the transcription.")
        return

    # Helper function to format milliseconds to SRT timestamp format
    def format_timestamp(ms):
        seconds, milliseconds = divmod(ms, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

    srt_lines = []
    for i, w in enumerate(words, start=1):
        start = format_timestamp(w.start)
        end = format_timestamp(w.end)
        srt_lines.append(f"{i}\n{start} --> {end}\n{w.text}\n")

    Path(output_file).write_text("\n".join(srt_lines), encoding="utf-8")
    print(f"Word-level SRT successfully saved to {output_file}")

# ==========================================
# Run the pipeline
# ==========================================
if __name__ == "__main__":
    # 1. Paste your YouTube URL here
    youtube_url = "https://www.youtube.com/watch?v=F_EWF1Ovmrc" 
    
    # 2. Define file names
    audio_filename = "downloaded_audio.mp3"
    srt_filename = "word_level_malayalam.srt"
    
    # 3. Execute
    downloaded_file = download_youtube_audio(youtube_url, audio_filename)
    
    if downloaded_file and os.path.exists(downloaded_file):
        # We pass language_code="ml" for Malayalam. Change to "en" if testing English videos.
        transcribe_word_level_srt(downloaded_file, srt_filename, language_code="ml")
        
        # Optional: Uncomment the next lines if you want to automatically delete the MP3 after transcribing to save space.
        # os.remove(downloaded_file)
        # print("Cleaned up temporary audio file.")