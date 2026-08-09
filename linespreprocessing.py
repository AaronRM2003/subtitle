import re

def merge_lines_by_timestamp(text):
    lines = text.split('\n')
    timestamp_pattern = re.compile(r'^\((\d{1,3}:\d{2})\)\s*')

    current_timestamp = None
    current_line = ""
    merged_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue  # skip empty lines

        match = timestamp_pattern.match(line)
        if match:
            new_timestamp = match.group(1)

            # Check if this is a new timestamp or the same one repeated
            if new_timestamp != current_timestamp:
                # If there was a previous timestamped line, save it before starting a new one
                if current_timestamp is not None:
                    merged_lines.append(f"({current_timestamp}) {current_line.strip()}")

                current_timestamp = new_timestamp
                current_line = line[match.end():].strip()  # Start a new merged sentence
            else:
                # Same timestamp → Append text to current line
                text_without_timestamp = line[match.end():].strip()
                if text_without_timestamp:
                    current_line += " " + text_without_timestamp
        else:
            # Append this line as continuation text
            if current_line:
                current_line += " " + line
            else:
                current_line = line

    # Append last entry after loop finishes
    if current_timestamp is not None:
        merged_lines.append(f"({current_timestamp}) {current_line.strip()}")

    return merged_lines


def main(input_filepath, output_filepath):
    with open(input_filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    merged = merge_lines_by_timestamp(text)

    with open(output_filepath, 'w', encoding='utf-8') as f:
        for line in merged:
            f.write(line + '\n')


if __name__ == "__main__":
    input_file = "transcript-english.txt"
    output_file = "transcript-english.txt"
    main(input_file, output_file)
    print(f"Processed lines written to {output_file}")
