from pathlib import Path
import json
import pysrt

EN_FOLDER = Path("yt_srt_output")
ML_FOLDER = EN_FOLDER / "original"

OUTPUT = EN_FOLDER / "translation_memory_raw"
OUTPUT.mkdir(exist_ok=True)

matched = 0

for ml_file in ML_FOLDER.glob("*.srt"):
    video_id = ml_file.stem
    en_file = EN_FOLDER / f"{video_id}.srt"

    if not en_file.exists():
        continue

    ml_subs = pysrt.open(str(ml_file), encoding="utf-8")
    en_subs = pysrt.open(str(en_file), encoding="utf-8")

    ml_text = "\n".join(
        s.text.replace("\n", " ").strip()
        for s in ml_subs
        if s.text.strip()
    )

    en_text = "\n".join(
        s.text.replace("\n", " ").strip()
        for s in en_subs
        if s.text.strip()
    )

    data = {
        "video": video_id,
        "malayalam": ml_text,
        "english": en_text,
    }

    with open(OUTPUT / f"{video_id}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    matched += 1

print(f"Matched {matched} testimony pairs.")