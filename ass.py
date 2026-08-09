import re

input_srt = "output.srt"   # your word-level SRT
output_ass = "output.ass"

ass_header = """[Script Info]
Title: Karaoke Subtitles
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,80,&H00FFFFFF,&H0000FFFF,&H00000000,&H98000000,-1,0,0,0,100,100,0,0,1,0,1,2,2,10,10,50,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def time_to_ass(ms):
    """Convert ms → ASS timestamp"""
    h = ms // 3600000
    m = (ms % 3600000) // 60000
    s = (ms % 60000) // 1000
    cs = (ms % 1000) // 10
    return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"

def parse_srt(srt_text):
    """Parse word-level SRT into list of dicts {text, start, end}"""
    srt_text = srt_text.replace("\r\n", "\n")
    words = []

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
            words.append({"text": text, "start": start, "end": end})

    return words

def make_windows(words, max_chars=20):
    """Group words into ~30-char windows"""
    windows = []
    i = 0
    while i < len(words):
        char_count = 0
        window_words = []
        start = words[i]["start"]
        end = words[i]["end"]

        while i < len(words) and char_count + len(words[i]["text"]) + 1 <= max_chars:
            window_words.append(words[i])
            char_count += len(words[i]["text"]) + 1
            end = words[i]["end"]
            i += 1

        windows.append({"words": window_words, "start": start, "end": end})
    return windows

def build_ass_events(windows):
    """
    Base line (Layer 0): full sentence in white, static for the window.
    Overlays (Layer 1): one Dialogue per word, timed to that word's start/end.
      - overlay text contains the whole sentence so spacing is preserved
      - non-target words are made fully transparent (\1a&HFF&)
      - the target word is visible and colored with \c (primary color)
    This produces: base white visible always, overlay appears only during word time
    showing that word in highlight, then disappears (transparent) again.
    """
    events = []
    for win in windows:
        # window start/end for the base line
        start = time_to_ass(win["start"])
        end = time_to_ass(win["end"])

        # Base (static) line: white text, bottom-center alignment (\an2), same margins
        base_text = " ".join(w["text"] for w in win["words"])
        events.append(f"Dialogue: 0,{start},{end},Default,,10,10,50,,{{\\an5}}{base_text}")


        # Per-word overlay dialogues (Layer 1) timed to each word individually
        for i, target in enumerate(win["words"]):
            w_start = time_to_ass(target["start"])
            w_end   = time_to_ass(target["end"])

            parts = []
            for j, w in enumerate(win["words"]):
                if i == j:
                    # target word: primary visible (alpha 00) and colored (use \c for primary color)
                    # keep overlay bord/shad 0 to avoid double-outline; set \an2 for exact alignment
                    parts.append(f"{{\\an5\\1a&H00&\\c&H00FFFF&\\bord0\\shad0}}{w['text']}")
                else:
                    # non-target words: make primary fully transparent so base shows through
                    parts.append(f"{{\\1a&HFF&}}{w['text']}")

            overlay_text = " ".join(parts)
            events.append(f"Dialogue: 1,{w_start},{w_end},Default,,10,10,50,,{overlay_text}")

    return "\n".join(events)


# Main
with open(input_srt, "r", encoding="utf-8") as f:
    srt_text = f.read()

words = parse_srt(srt_text)
windows = make_windows(words)
ass_events = build_ass_events(windows)

with open(output_ass, "w", encoding="utf-8") as f:
    f.write(ass_header + "\n" + ass_events)

print(f"ASS file created: {output_ass}")
