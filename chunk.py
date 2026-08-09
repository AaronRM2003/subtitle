from pathlib import Path
import pysrt
import json
import math
import re

EN_FOLDER = Path("yt_srt_output")
ML_FOLDER = EN_FOLDER / "original"

OUTPUT = EN_FOLDER / "translation_memory.json"


def load_srt(path):
    subs = pysrt.open(str(path), encoding="utf-8")

    text = []

    for s in subs:
        t = s.text.replace("\\N", " ")
        t = t.replace("\n", " ")
        t = re.sub(r"\s+", " ", t).strip()

        if t:
            text.append(t)

    return text


def split_equal(lines, parts):
    """
    Split into approximately equal parts,
    preserving whole subtitle lines.
    """

    total_chars = sum(len(x) for x in lines)

    target = total_chars / parts

    result = []
    current = []
    current_chars = 0

    for line in lines:

        current.append(line)
        current_chars += len(line)

        if current_chars >= target and len(result) < parts - 1:
            result.append(" ".join(current))
            current = []
            current_chars = 0

    if current:
        result.append(" ".join(current))

    return result


memory = []

matched = 0

for ml_file in sorted(ML_FOLDER.glob("*.srt")):

    video = ml_file.stem

    en_file = EN_FOLDER / f"{video}.srt"

    if not en_file.exists():
        continue

    ml_lines = load_srt(ml_file)
    en_lines = load_srt(en_file)

    # choose number of parts based on length
    total = max(len(ml_lines), len(en_lines))

    if total < 250:
        parts = 6
    elif total < 500:
        parts = 8
    else:
        parts = 10

    ml_chunks = split_equal(ml_lines, parts)
    en_chunks = split_equal(en_lines, parts)

    # in case one side produced fewer chunks
    n = min(len(ml_chunks), len(en_chunks))

    for i in range(n):

        memory.append(
            {
                "video": video,
                "part": i + 1,
                "total_parts": n,
                "ml": ml_chunks[i],
                "en": en_chunks[i],
            }
        )

    matched += 1

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(memory, f, ensure_ascii=False, indent=2)

print(f"Matched testimonies : {matched}")
print(f"Translation memory entries : {len(memory)}")
print(f"Saved to {OUTPUT}")