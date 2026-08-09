import re

def update_timestamps_in_file(filename, output_filename=None):
    # Read the content of the file
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    # Replace timestamps like 00:00 with (0:00)
    updated_content = re.sub(r'\b(\d{1,2}):(\d{2})\b', r'(\1:\2)', content)

    # Write to the same file or a new file
    output_file = output_filename if output_filename else filename
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(updated_content)

    print(f"Timestamps updated successfully in '{output_file}'.")

# Example usage:
update_timestamps_in_file('transcript-english.txt')  # overwrites the file
# Or:
# update_timestamps_in_file('transcript.txt', 'updated_transcript.txt')  # creates new file
