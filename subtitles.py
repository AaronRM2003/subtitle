import os

# Input SRT and output ASS
srt_file = "output.srt"
ass_file = "video/subtitles.ass"

# Subtitle style settings for Instagram vertical video
font_name = "Arial"
font_size = 70           # Big but fits within width
primary_color = "&H00FFFFFF"  # White text
outline_color = "&H00FFFFFF"  # Black outline
outline = 4               # Thick outline for readability
shadow = 0
alignment = 2             # Bottom-center
margin_v = 100            # Vertical margin from bottom
margin_h = 200            # Horizontal margins for wrapping
bold = 1

# ASS file header
ass_header = f"""[Script Info]
Title: Instagram Vertical Subtitles
ScriptType: v4.00+
Collisions: Normal
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font_name},{font_size},{primary_color},&H000000FF,{outline_color},&H00000000,{bold},0,0,0,100,100,0,0,1,{outline},{shadow},{alignment},{margin_h},{margin_h},{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def srt_time_to_ms(time_str):
    """Convert SRT time 00:00:01,500 to milliseconds"""
    h, m, s_ms = time_str.split(":")
    s, ms = s_ms.split(",")
    return int(h)*3600000 + int(m)*60000 + int(s)*1000 + int(ms)

def ms_to_ass(ms):
    """Convert milliseconds to ASS time 0:00:01.50"""
    h = ms // 3600000
    ms %= 3600000
    m = ms // 60000
    ms %= 60000
    s = ms // 1000
    ms %= 1000
    cs = ms // 10  # centiseconds
    return f"{h}:{m:02}:{s:02}.{cs:02}"

# Read SRT
with open(srt_file, "r", encoding="utf-8") as f:
    lines = f.read().splitlines()

# Find first subtitle start time for offset
first_start_ms = None
i = 0
while i < len(lines):
    if lines[i].isdigit():
        i += 1
        if i >= len(lines):
            break
        times = lines[i].split(" --> ")
        start_ms = srt_time_to_ms(times[0].strip())
        if first_start_ms is None:
            first_start_ms = start_ms
        break
    i += 1

# Convert SRT to ASS with offset and word wrap
ass_events = ""
i = 0
while i < len(lines):
    if lines[i].isdigit():
        i += 1
        if i >= len(lines):
            break
        times = lines[i].split(" --> ")
        start = ms_to_ass(srt_time_to_ms(times[0].strip()) - first_start_ms)
        end = ms_to_ass(srt_time_to_ms(times[1].strip()) - first_start_ms)
        i += 1
        text_lines = []
        while i < len(lines) and lines[i].strip() != "":
            text_lines.append(lines[i].strip())
            i += 1
        # Join lines with \N for manual line breaks, add \q2 for automatic wrapping
        text = "{\\q2}" + "\\N".join(text_lines)
        ass_events += f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n"
    else:
        i += 1

# Write ASS
os.makedirs(os.path.dirname(ass_file), exist_ok=True)
with open(ass_file, "w", encoding="utf-8") as f:
    f.write(ass_header)
    f.write(ass_events)

print(f"Converted {srt_file} → {ass_file} with Instagram-ready vertical subtitles!")
