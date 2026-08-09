import re

def time_to_seconds(mm, ss):
    return int(mm) * 60 + int(ss)

def seconds_to_time(seconds):
    mm = int(seconds // 60)
    ss = int(seconds % 60)
    return f"{mm:02}:{ss:02}"

def adjust_txt_timing(input_file, output_file, speed):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    updated_lines = []

    for line in lines:
        match = re.search(r'\((\d{2}):(\d{2})\)', line)
        if match:
            mm, ss = match.groups()
            total_sec = time_to_seconds(mm, ss)

            # adjust timing
            new_time = total_sec / speed

            new_timestamp = seconds_to_time(new_time)

            # replace old time with new time
            line = re.sub(r'\(\d{2}:\d{2}\)', f'({new_timestamp})', line)

        updated_lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)

    print("✅ TXT subtitles adjusted successfully!")


# ===== USAGE =====
input_file = "output_clean.txt"
speed = 1.25   # change this

adjust_txt_timing(input_file, input_file, speed)