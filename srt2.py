import re
from datetime import timedelta

# -----------------------------
# TIME HELPERS
# -----------------------------
def parse_timestamp(timestamp):
    minutes, seconds = map(int, timestamp.split(":"))
    return timedelta(minutes=minutes, seconds=seconds)

def format_srt_time(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02},000"

# -----------------------------
# PARSE INPUT
# -----------------------------
def extract_subs(lines):
    subs = []
    for line in lines:
        match = re.match(r"\((\d+:\d+)\)\s*(.+)", line.strip())
        if match:
            subs.append((match.group(1), match.group(2).strip()))
    return subs

# -----------------------------
# SIMPLE SRT CONVERSION
# -----------------------------
def convert_to_srt(input_file, output_file, default_duration=4):
    with open(input_file, "r", encoding="utf-8") as f:
        subs = extract_subs(f.readlines())

    srt_lines = []

    for i, (timestamp, text) in enumerate(subs):
        start = parse_timestamp(timestamp)

        if i < len(subs) - 1:
            end = parse_timestamp(subs[i + 1][0])
        else:
            end = start + timedelta(seconds=default_duration)

        srt_lines.append(
            f"{i+1}\n"
            f"{format_srt_time(start)} --> {format_srt_time(end)}\n"
            f"{text}\n"
        )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_lines))

    print(f"✅ Created: {output_file}")

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    convert_to_srt(
        input_file="transcript-english.txt",
        output_file="output.srt"
    )