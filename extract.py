import json
import os
import re
from pathlib import Path

# =====================================================
# CONFIGURATION
# =====================================================

# Main JSON file
MAIN_JSON = r"C:\Users\mincy\Desktop\kreupasanam\my-testimonies-site\public\assets\testimony-content.json"  # path to your main JSON file

# Folder containing files like 20apr26.json
SUBTITLE_FOLDER = r"C:\Users\mincy\Desktop\kreupasanam\my-testimonies-site\public\assets\testimony-subtitle"

# Output folder
OUTPUT_FOLDER = r"yt_srt_output"

# Language to export
LANGUAGE = "en"

# =====================================================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def extract_video_id(url):
    m = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", url)
    return m.group(1) if m else None


def parse_time(t):
    """
    Converts:
        0:10
        1:02
        10:05
        1:02:30
        0:10.5

    into milliseconds
    """

    parts = t.split(":")

    if len(parts) == 2:
        h = 0
        m = int(parts[0])
        s = float(parts[1])
    elif len(parts) == 3:
        h = int(parts[0])
        m = int(parts[1])
        s = float(parts[2])
    else:
        raise ValueError(f"Invalid time: {t}")

    return int((h * 3600 + m * 60 + s) * 1000)


def ms_to_srt(ms):
    h = ms // 3600000
    ms %= 3600000

    m = ms // 60000
    ms %= 60000

    s = ms // 1000
    ms %= 1000

    return f"{h:02}:{m:02}:{s:02},{ms:03}"


with open(MAIN_JSON, encoding="utf-8") as f:
    videos = json.load(f)

for video in videos:

    youtube_id = extract_video_id(video["video"])

    if youtube_id is None:
        print("Couldn't parse:", video["video"])
        continue

    subtitle_filename = Path(video["subtitles"]).name
    subtitle_path = os.path.join(SUBTITLE_FOLDER, subtitle_filename)

    if not os.path.exists(subtitle_path):
        print("Missing:", subtitle_filename)
        continue

    with open(subtitle_path, encoding="utf-8") as f:
        subs = json.load(f)

    output = []

    for i, item in enumerate(subs):

        start_ms = parse_time(item["start"])

        if i < len(subs) - 1:
            end_ms = parse_time(subs[i + 1]["start"]) - 1
        else:
            end_ms = start_ms + 4000

        text = item["text"].get(LANGUAGE, "").strip()

        output.append(
            f"{i+1}\n"
            f"{ms_to_srt(start_ms)} --> {ms_to_srt(end_ms)}\n"
            f"{text}\n"
        )

    out_file = os.path.join(OUTPUT_FOLDER, youtube_id + ".srt")

    with open(out_file, "w", encoding="utf-8-sig") as f:
        f.write("\n".join(output))

    print("Created", out_file)

print("Done!")