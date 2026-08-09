import re

def normalize_timestamp(ts: str) -> str:
    parts = ts.split(":")

    # hh:mm:ss → total_minutes:ss
    if len(parts) == 3:
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = parts[2]
        total_minutes = hours * 60 + minutes
        return f"{total_minutes}:{seconds}"

    # mm:ss (or big minutes)
    elif len(parts) == 2:
        return f"{int(parts[0])}:{parts[1]}"

    return ts

def convert_text(text: str) -> str:
    lines = text.splitlines()
    result = []
    current_time = None

    time_pattern = re.compile(r"^\d+:\d{2}(:\d{2})?$")

    for line in lines:
        stripped = line.strip()

        if time_pattern.match(stripped):
            current_time = f"({normalize_timestamp(stripped)})"
        elif stripped and current_time:
            result.append(f"{current_time} {stripped}")
            current_time = None
        elif stripped:
            result.append(stripped)

    return "\n".join(result)

def update_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    updated = convert_text(content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(updated)

    print("File updated successfully.")

if __name__ == "__main__":
    file_path = "transcript-english.txt"   # change if needed
    update_file(file_path)
