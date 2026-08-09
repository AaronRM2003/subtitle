import re
import textwrap

input_srt = "output.srt"
output_ass = "output.ass"

# NOTE: ASS color format is &HAABBGGRR (Alpha, Blue, Green, Red)
# Violet box example (nice purple)
VIOLET_BOX = "&H002A1A6D"   # deep violet (tweak if needed)
WHITE_TEXT = "&H00FFFFFF"

ass_header = f"""[Script Info]
Title: Violet Box Subtitles (Insta Safe + Wrapped)
ScriptType: v4.00+
Collisions: Normal
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, \
        Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, \
        Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding

; BorderStyle=3 => solid box using BackColour
; Outline => padding of box
; Alignment=8 => TOP-CENTER (so it's inside the video and not hidden by Instagram UI)
Style: Default,Times New Roman,53,&H00FFFFFF,&H00000000,&H006B6BFF ,&H00000000,\
       1,0,0,0,100,100,0,0,3,26,0,2,100,100,400,1


[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def time_to_ass(ms):
    h = ms // 3600000
    m = (ms % 3600000) // 60000
    s = (ms % 60000) // 1000
    cs = (ms % 1000) // 10
    return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"

def parse_srt(srt_text):
    srt_text = srt_text.replace("\r\n", "\n")
    subs = []
    for block in re.split(r"\n\n+", srt_text.strip()):
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        times = lines[1]
        m = re.match(r"(\d+):(\d+):(\d+),(\d+)\s*-->\s*(\d+):(\d+):(\d+),(\d+)", times)
        if not m:
            continue
        start = (int(m[1])*3600 + int(m[2])*60 + int(m[3]))*1000 + int(m[4])
        end   = (int(m[5])*3600 + int(m[6])*60 + int(m[7]))*1000 + int(m[8])
        text  = " ".join(lines[2:]).strip()
        if text:
            subs.append({"text": text, "start": start, "end": end})
    return subs

def wrap_text_for_insta(text, width=34, max_lines=5):
    """
    Hard wrap for Instagram so text NEVER runs outside screen.
    width=34 works good for 1080x1920 with fontsize ~52.
    """
    text = text.strip()
    wrapped = textwrap.wrap(text, width=width)

    # Limit lines
    if len(wrapped) > max_lines:
        wrapped = wrapped[:max_lines]
        # add ellipsis on last line
        if len(wrapped[-1]) > 3:
            wrapped[-1] = wrapped[-1][:-3] + "..."

    return r"\N".join(wrapped)

def build_ass_events(subs, offset=True):
    events = []
    base_time = subs[0]["start"] if (offset and subs) else 0

    for sub in subs:
        start = time_to_ass(sub["start"] - base_time)
        end   = time_to_ass(sub["end"] - base_time)

        text = sub["text"].replace("{", "").replace("}", "")
        text = wrap_text_for_insta(text, width=34, max_lines=5)

        # \an8 => top center
        # \fad => smooth fade
        styled_text = f"{{\\an2\\fad(180,180)}}{text}"
        events.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{styled_text}")

    return "\n".join(events)

# Main
with open(input_srt, "r", encoding="utf-8") as f:
    srt_text = f.read()

subs = parse_srt(srt_text)
ass_events = build_ass_events(subs, offset=True)

with open(output_ass, "w", encoding="utf-8") as f:
    f.write(ass_header + "\n" + ass_events)

print(f"ASS file created (violet box + wrapped + insta safe): {output_ass}")
