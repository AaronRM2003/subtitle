from datetime import timedelta
import re

input_file = "output_clean.txt"
output_file = "output_clean.txt"

# Time offset
time_offset = timedelta(minutes= -14,seconds=-55)

# Match only timestamps inside parentheses
timestamp_pattern = re.compile(r'\((\d{1,2}:\d{2})\)')

def adjust_timestamp(match):
    timestamp = match.group(1)
    minute, second = map(int, timestamp.split(':'))

    dt = timedelta(minutes=minute, seconds=second)
    dt_new = dt + time_offset

    # Clamp negative timestamps to 0:00
    if dt_new.total_seconds() < 0:
        dt_new = timedelta(seconds=0)

    total_seconds = int(dt_new.total_seconds())
    new_minute = total_seconds // 60
    new_second = total_seconds % 60

    # Minutes without leading zero
    return f"({new_minute}:{new_second:02d})"


with open(input_file, 'r', encoding='utf-8') as f:
    text = f.read()

new_text = timestamp_pattern.sub(adjust_timestamp, text)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(new_text)

print(f"Timestamps adjusted and saved to {output_file}")