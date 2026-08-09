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
# PARSE INPUT LINES INTO STRUCTURED FORM
# -----------------------------
def extract_subs(lines):
    subs = []
    for line in lines:
        match = re.match(r"\((\d+:\d+)\)\s*(.+)", line.strip())
        if match:
            subs.append([match.group(1), match.group(2).strip()])
    return subs

def convert_to_srt(subs, default_duration=4):
    srt_lines = []
    for i in range(len(subs)):
        start = parse_timestamp(subs[i][0])
        text = subs[i][1]

        if i < len(subs) - 1:
            end = parse_timestamp(subs[i + 1][0])
        else:
            end = start + timedelta(seconds=default_duration)

        srt_lines.append(
            f"{i+1}\n"
            f"{format_srt_time(start)} --> {format_srt_time(end)}\n"
            f"{text}\n"
        )
    return "\n".join(srt_lines)

end_marks = ('.', '!', '?', ',', ';', '…')
closing_quotes = ('"', '”')

def find_borrow_length(next_text):
    for idx, ch in enumerate(next_text):
        if ch in end_marks:
            if idx + 1 < len(next_text) and next_text[idx + 1] in closing_quotes:
                return idx + 2
            return idx + 1
        if ch in closing_quotes:
            return idx + 1
    return -1

def ends_with_punctuation_or_quote(text):
    text = text.rstrip()
    if text.endswith(end_marks):
        return True
    if text and text[-1] in closing_quotes:
        inner = text[:-1].rstrip()
        if inner.endswith(end_marks) or inner:
            return True
    return False

# -----------------------------
# NEW ADVANCED RULES
# -----------------------------
def apply_advanced_rules(subs):
    # Rule 1: Combine subtitles if the duration is < 3 seconds
    i = 0
    while i < len(subs) - 1:
        start_current = parse_timestamp(subs[i][0])
        start_next = parse_timestamp(subs[i+1][0])
        duration = (start_next - start_current).total_seconds()

        if duration < 3:
            # e.g. 1:17 and 1:19 (2 seconds apart) will merge here
            subs[i][1] = f"{subs[i][1].strip()} {subs[i+1][1].strip()}"
            subs.pop(i+1) 
        else:
            i += 1

    # Rule 2: Move short starting phrase (<= 3 words, ends in punctuation) to previous
    i = 1
    while i < len(subs):
        text = subs[i][1].strip()
        
        if len(text.split()) > 8:
            # Match: (Phrase up to first .?!) + space + (Rest of text)
            match = re.match(r'^([^.?!]+[.?!])\s+(.*)', text)
            if match:
                first_part = match.group(1).strip()
                rest_part = match.group(2).strip()
                
                # If first sentence is 3 words or less, push it back
                if len(first_part.split()) <= 3 and any(c.isalpha() for c in first_part):
                    subs[i-1][1] = f"{subs[i-1][1].strip()} {first_part}"
                    subs[i][1] = rest_part
        i += 1

    # Rule 3: Move short ending phrase (<= 3 words, AFTER a punctuation mark) to next
    i = 0
    while i < len(subs) - 1:
        text = subs[i][1].strip()
        
        # Match: (Everything up to the LAST .?!) + space + (Trailing leftover words)
        # e.g., Group 1: "...beautiful adoration." | Group 2: "O Lord,"
        match = re.search(r'(.*[.?!])\s+([^.?!]*)$', text)
        if match:
            main_part = match.group(1).strip()
            trailing_part = match.group(2).strip()
            
            # If the leftover trailing part is 3 words or less, push it forward
            if 0 < len(trailing_part.split()) <= 3 and any(c.isalpha() for c in trailing_part):
                subs[i+1][1] = f"{trailing_part} {subs[i+1][1].strip()}"
                subs[i][1] = main_part
        i += 1

    return subs

def enforce_punctuation_rules(subs, max_words=35):
    for i in range(len(subs) - 1):
        ts, text = subs[i]
        text = text.strip()

        if ends_with_punctuation_or_quote(text):
            continue

        next_ts, next_text = subs[i + 1]
        next_text = next_text.strip()

        cut_index = find_borrow_length(next_text)

        if cut_index == -1:
            continue

        borrow_part = next_text[:cut_index + 1].strip()
        remaining = next_text[cut_index + 1:].lstrip()

        if not remaining:
            continue

        text = re.sub(r'(\.\.\.|…)$', '', text).rstrip()
        merged = text + " " + borrow_part

        if len(merged.split()) > max_words:
            continue

        subs[i][1] = merged
        subs[i + 1][1] = remaining

    return subs

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    input_file = "transcript-english.txt"
    output_file = "output.srt"

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # 1. extract raw subtitles
        subs = extract_subs(lines)
        
        # 2. apply new duration (< 3s) and sentence shift rules FIRST
        subs = apply_advanced_rules(subs)
        
        # 3. apply standard punctuation borrowing rules SECOND
        subs = enforce_punctuation_rules(subs)

        # 4. convert to SRT
        srt_content = convert_to_srt(subs)

        # 5. save file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(srt_content)

        print(f"✅ SRT file created: {output_file}")
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{input_file}'. Please make sure the file exists in the same directory.")