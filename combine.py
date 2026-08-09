import re
from datetime import datetime

# Malayalam sentence-ending markers
sentence_endings = ['.']

def is_complete_sentence(text):
    """Check if a Malayalam line ends with a sentence-ending marker."""
    text = text.strip()
    return any(text.endswith(end) for end in sentence_endings)

def read_srt(file_path):
    """Read subtitles from an .srt/.txt file into a list of (index, timestamp, text)."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = re.split(r'\n\s*\n', content.strip())
    subtitles = []

    for block in blocks:
        lines = block.strip().splitlines()
        if len(lines) >= 3:
            index = lines[0]
            timestamp = lines[1]
            text = ' '.join(lines[2:]).strip()
            subtitles.append((index, timestamp, text))
    
    return subtitles

def srt_time_to_seconds(srt_time):
    """Convert SRT timestamp to total seconds."""
    time_obj = datetime.strptime(srt_time, "%H:%M:%S,%f")
    return int(time_obj.hour) * 3600 + int(time_obj.minute) * 60 + int(time_obj.second)

def format_time_bracket(srt_time):
    """Convert SRT time to (M:SS) format."""
    total_seconds = srt_time_to_seconds(srt_time)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"({minutes}:{str(seconds).zfill(2)})"

def combine_subtitles(subtitles, max_lines=2):
    """Combine subtitle lines and prefix with (M:SS) timestamp."""
    combined = []
    buffer_text = []
    buffer_start = None
    buffer_end = None

    for idx, ts, txt in subtitles:
        start_time, end_time = ts.split(" --> ")
        if not buffer_text:
            buffer_start = start_time
        buffer_end = end_time
        buffer_text.append(txt)

        if is_complete_sentence(txt) or len(buffer_text) >= max_lines:
            start_bracket = format_time_bracket(buffer_start)
            combined_text = start_bracket + ' ' + ' '.join(buffer_text).strip()
            combined.append((buffer_start, buffer_end, combined_text))
            buffer_text = []

    # Add leftover buffer
    if buffer_text:
        start_bracket = format_time_bracket(buffer_start)
        combined_text = start_bracket + ' ' + ' '.join(buffer_text).strip()
        combined.append((buffer_start, buffer_end, combined_text))

    return combined

def write_combined_srt(combined_subs, output_file):
    """Write only cleaned subtitle lines with (M:SS) timestamp."""
    with open(output_file, 'w', encoding='utf-8') as f:
        for start, _, txt in combined_subs:
            f.write(f"{txt}\n")

# =========================
# 🔧 Usage

input_file = 'output.srt'         # Your input file
output_file = 'transcript-english.txt' # Final cleaned output

subs = read_srt(input_file)
combined_subs = combine_subtitles(subs, max_lines=1)
write_combined_srt(combined_subs, output_file)
