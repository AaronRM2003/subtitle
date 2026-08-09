import yt_dlp
import librosa
import numpy as np
import soundfile as sf
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

# ---------------------------------------------------
# 1. Download Audio
# ---------------------------------------------------

def download_audio(url, name):

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{name}.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


# ---------------------------------------------------
# 2. Detect Speech Segments
# ---------------------------------------------------

def detect_segments(file):

    audio = AudioSegment.from_wav(file)

    segments = detect_nonsilent(
        audio,
        min_silence_len=200,
        silence_thresh=audio.dBFS - 16
    )

    return segments


# ---------------------------------------------------
# 3. Convert segments to chunks
# ---------------------------------------------------

def extract_chunks(file, segments):

    audio = AudioSegment.from_wav(file)

    chunks = []

    for start,end in segments:

        chunks.append(audio[start:end])

    return chunks


# ---------------------------------------------------
# 4. Convert pydub -> numpy
# ---------------------------------------------------

def audiosegment_to_numpy(chunk):

    samples = np.array(chunk.get_array_of_samples()).astype(np.float32)

    sr = chunk.frame_rate

    return samples, sr


# ---------------------------------------------------
# 5. Time stretch with limits
# ---------------------------------------------------

def stretch_to_duration(chunk, target_duration):

    samples, sr = audiosegment_to_numpy(chunk)

    current_duration = len(samples)/sr

    rate = current_duration / target_duration

    if rate < 0.5:
        rate = 0.5

    if rate > 2:
        rate = 2

    stretched = librosa.effects.time_stretch(samples, rate=rate)

    return stretched, sr


# ---------------------------------------------------
# 6. numpy -> pydub
# ---------------------------------------------------

def numpy_to_audiosegment(samples, sr):

    samples = samples.astype(np.int16)

    audio = AudioSegment(
        samples.tobytes(),
        frame_rate=sr,
        sample_width=2,
        channels=1
    )

    return audio


# ---------------------------------------------------
# 7. Compute MFCC features
# ---------------------------------------------------

def mfcc_features(file):

    y, sr = librosa.load(file)

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    return mfcc


# ---------------------------------------------------
# 8. DTW Alignment
# ---------------------------------------------------

def align_dtw(orig_file, dub_file):

    y1, sr1 = librosa.load(orig_file, sr=8000)
    y2, sr2 = librosa.load(dub_file, sr=8000)

    mfcc_orig = librosa.feature.mfcc(
        y=y1,
        sr=sr1,
        n_mfcc=13,
        hop_length=2048
    ).astype(np.float32)

    mfcc_dub = librosa.feature.mfcc(
        y=y2,
        sr=sr2,
        n_mfcc=13,
        hop_length=2048
    ).astype(np.float32)

    D, wp = librosa.sequence.dtw(
        mfcc_orig,
        mfcc_dub,
        metric="euclidean",
        global_constraints=True,
        band_rad=0.25
    )

    return np.array(wp)

# ---------------------------------------------------
# 9. Build Synced Audio
# ---------------------------------------------------

def build_synced_audio(orig_segments, dub_chunks):

    final_audio = AudioSegment.empty()

    dub_index = 0

    for i in range(len(orig_segments)):

        start,end = orig_segments[i]

        target_duration = (end-start)/1000

        if dub_index < len(dub_chunks):

            chunk = dub_chunks[dub_index]

            stretched, sr = stretch_to_duration(chunk, target_duration)

            new_chunk = numpy_to_audiosegment(stretched, sr)

            final_audio += new_chunk

            dub_index += 1

        else:

            final_audio += AudioSegment.silent(duration=end-start)

        # pause
        if i < len(orig_segments)-1:

            next_start = orig_segments[i+1][0]

            pause = next_start-end

            if pause > 0:

                final_audio += AudioSegment.silent(duration=pause)

    return final_audio


# ---------------------------------------------------
# 10. Global duration correction
# ---------------------------------------------------

def global_adjust(audio, target_duration):

    samples = np.array(audio.get_array_of_samples()).astype(np.float32)

    sr = audio.frame_rate

    current = len(samples)/sr

    rate = current/target_duration

    stretched = librosa.effects.time_stretch(samples, rate)

    return numpy_to_audiosegment(stretched, sr)


# ---------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------

original_url = "https://youtu.be/AGCMbEPfYoA"
dub_url = "https://youtu.be/YjauqobTdUA"

print("Downloading audio...")

download_audio(original_url,"original")
download_audio(dub_url,"dub")


print("Detecting speech segments...")

orig_segments = detect_segments("original.wav")
dub_segments = detect_segments("dub.wav")


print("Extracting dub chunks...")

dub_chunks = extract_chunks("dub.wav", dub_segments)


print("Aligning audio (DTW)...")

alignment = align_dtw("original.wav","dub.wav")


print("Building synced dub...")

final_audio = build_synced_audio(orig_segments, dub_chunks)


print("Final duration correction...")

orig_audio = AudioSegment.from_wav("original.wav")

target_duration = len(orig_audio)/1000

final_audio = global_adjust(final_audio, target_duration)


print("Exporting result...")

final_audio.export("dub_synced.wav", format="wav")

print("DONE")