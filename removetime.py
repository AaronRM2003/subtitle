import re

# ✅ Hardcoded file names
input_file = "output_clean.txt"    # Change this to your input file name
output_file = "output_clean.txt"     # Change this to your desired output file name

def remove_timestamps(text):
    # Remove timestamps with surrounding spaces (but NOT newlines)
    pattern = r"[ \t]*\(\d+:\d{2}(?::\d{2})?\)[ \t]*"
    text = re.sub(pattern, " ", text)

    # Clean multiple spaces (but not line breaks)
    text = re.sub(r"[ ]{2,}", " ", text)

    # Remove leading spaces at each line
    text = re.sub(r"(?m)^[ \t]+", "", text)

    return text.strip()

def process_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    cleaned = remove_timestamps(content)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned)

    print(f"Done! Cleaned file saved to: {output_path}")

# Run the processing
process_file(input_file, output_file)
