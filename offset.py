import os

# Input/output files
srt_file = "output.srt"          # your original SRT file
output_srt_file = "output.srt" # output file
# Option 1: desired start time for first subtitle in milliseconds
desired_start_ms = 4000  # 5 seconds → 5000 ms, change to 7000 for 7 seconds

# Option 2: fixed offset in milliseconds (comment out Option 1 if using this)
# offset_ms = -5000  # shift all subtitles 5 seconds earlier

def srt_time_to_ms(time_str):
    """Convert SRT time format to milliseconds"""
    h, m, s_ms = time_str.split(":")
    s, ms = s_ms.split(",")
    return int(h)*3600000 + int(m)*60000 + int(s)*1000 + int(ms)

def ms_to_srt(ms):
    """Convert milliseconds to SRT time format"""
    h = ms // 3600000
    ms %= 3600000
    m = ms // 60000
    ms %= 60000
    s = ms // 1000
    ms %= 1000
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

# Read all lines
with open(srt_file, "r", encoding="utf-8") as f:
    lines = f.read().splitlines()

# Find the first subtitle time
first_start_ms = None
for line in lines:
    if "-->" in line:
        start_time = line.split(" --> ")[0].strip()
        first_start_ms = srt_time_to_ms(start_time)
        break

if first_start_ms is None:
    raise ValueError("No subtitle timings found in file!")

# Calculate offset based on desired start (Option 1)
offset_ms = desired_start_ms - first_start_ms

# Apply offset
output_lines = []
for line in lines:
    if "-->" in line:
        start, end = line.split(" --> ")
        start_ms = srt_time_to_ms(start.strip()) + offset_ms
        end_ms = srt_time_to_ms(end.strip()) + offset_ms
        # Ensure no negative times
        start_ms = max(0, start_ms)
        end_ms = max(0, end_ms)
        output_lines.append(f"{ms_to_srt(start_ms)} --> {ms_to_srt(end_ms)}")
    else:
        output_lines.append(line)

# Save new shifted SRT
with open(output_srt_file, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print(f"Shifted subtitles saved to {output_srt_file}")
