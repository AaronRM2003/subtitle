import re

def parse_time(ts):
    """Convert mm:ss or m:ss to total seconds."""
    m, s = map(int, ts.split(":"))
    return m * 60 + s

def format_time(seconds):
    """Format seconds back to (mm:ss)."""
    minutes = seconds // 60
    sec = seconds % 60
    return f"({minutes}:{sec:02d})"

def adjust_subtitles(lines, total_duration=None):
    """
    lines = ['(4:00) text...', '(4:08) text...', ...]
    Returns list of ('(mm:ss)', sentence).
    """

    # 1) Extract timestamps + subtitles
    timestamps = []
    texts = []
    for line in lines:
        m = re.match(r"\(?(\d+:\d+)\)?\s*(.*)", line.strip())
        if m:
            timestamps.append(parse_time(m.group(1)))
            texts.append(m.group(2).strip())

    # Determine duration
    if total_duration is None:
        total_duration = timestamps[-1] + 3  # last timestamp + buffer

    start_time = timestamps[0]

    # 2) Combine all text & split by sentences
    combined = " ".join(texts)
    sentences = re.split(r'(?<=[.!?])\s+', combined)
    sentences = [s.strip() for s in sentences if s.strip()]

    # 3) Distribute timestamps proportional to text length
    total_chars = sum(len(s) for s in sentences)

    results = []
    current_sec = start_time

    for s in sentences:
        proportion = len(s) / total_chars
        dur = proportion * (total_duration - start_time)

        results.append((format_time(int(current_sec)), s))
        current_sec += dur

    return results


# ---------------- USE THIS SECTION ----------------

# Read input file
with open("output_clean.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Process subtitles
result = adjust_subtitles(lines)

# Write output file
with open("output_clean.txt", "w", encoding="utf-8") as f:
    for ts, text in result:
        f.write(f"{ts} {text}\n")

