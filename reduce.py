import re

def time_str_to_seconds(time_str):
    """Convert (m:ss) to total seconds."""
    m, s = map(int, time_str.strip("()").split(":"))
    return m * 60 + s

def seconds_to_time_str(seconds):
    """Convert seconds to (m:ss) format."""
    m = seconds // 60
    s = seconds % 60
    return f"({m}:{s:02})"

def split_subtitles(input_file, output_file, max_words=30, default_duration=5):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    new_lines = []
    for i, line in enumerate(lines):
        match = re.match(r'\((\d+:\d+)\)\s*(.*)', line)
        if not match:
            new_lines.append(line + '\n')
            continue

        start_time_str, text = match.groups()
        words = text.split()
        start_sec = time_str_to_seconds(start_time_str)

        # Calculate duration to next subtitle
        if i + 1 < len(lines):
            next_match = re.match(r'\((\d+:\d+)\)', lines[i + 1])
            if next_match:
                end_sec = time_str_to_seconds(next_match.group(1))
            else:
                end_sec = start_sec + default_duration
        else:
            end_sec = start_sec + default_duration

        if len(words) > max_words:
            mid = len(words) // 2
            first_half = ' '.join(words[:mid])
            second_half = ' '.join(words[mid:])

            mid_sec = start_sec + (end_sec - start_sec) // 2

            # Append both halves with updated timestamps
            new_lines.append(f"{seconds_to_time_str(start_sec)} {first_half}\n")
            new_lines.append(f"{seconds_to_time_str(mid_sec)} {second_half}\n")
        else:
            new_lines.append(line + '\n')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

# Usage
split_subtitles('transcript-english.txt', 'transcript-english.txt')
