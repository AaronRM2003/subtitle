import math
import re

# === USER SETTINGS ===
INPUT_FILE = "transcript-english.txt"      # Original subtitle text file
NUMBER_OF_GROUPS = 7          # Final number of timestamps required
# =====================

timestamp_pattern = re.compile(r"^\(\d+:\d+\)")

def read_entries():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines

def group_and_merge(entries, group_count):
    total = len(entries)
    per_group = math.ceil(total / group_count)
    
    merged = []
    
    for i in range(0, total, per_group):
        block = entries[i:i + per_group]
        first_timestamp = timestamp_pattern.match(block[0]).group(0)
        
        subtitles = []
        for line in block:
            text = timestamp_pattern.sub("", line).strip()
            subtitles.append(text)
        
        merged.append(f"{first_timestamp} " + " ".join(subtitles))
    
    return merged

def write_back(results):
    with open(INPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(results))
    print(f"Updated '{INPUT_FILE}' with {len(results)} merged timestamps.")

def main():
    entries = read_entries()
    merged = group_and_merge(entries, NUMBER_OF_GROUPS)
    write_back(merged)

if __name__ == "__main__":
    main()
