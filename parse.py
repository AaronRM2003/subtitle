import re
import json
from collections import OrderedDict

# Language files
language_files = {
    'en': 'transcript-english.txt',
    'hi': 'transcript-hindi.txt',
    'ta': 'transcript-tamil.txt',
    'bn': 'transcript-bengali.txt',
    'te': 'transcript-telugu.txt',
    'mr': 'transcript-marathi.txt',
    'fr': 'transcript-french.txt',
    'es': 'transcript-spanish.txt',
    'zh': 'transcript-chinese.txt',
    'kn': 'transcript-kannada.txt',
}

# Digit normalization map
digit_map = {
    '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
    '५': '5', '६': '6', '७': '7', '८': '8', '९': '9',
    '০': '0', '১': '1', '২': '2', '৩': '3', '৪': '4',
    '৫': '5', '৬': '6', '৭': '7', '৮': '8', '৯': '9',
    '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
    '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9',
    '೦': '0', '೧': '1', '೨': '2', '೩': '3', '೪': '4',
    '೫': '5', '೬': '6', '೭': '7', '೮': '8', '೯': '9',
}

def normalize_text(text):
    text = text.replace('（', '(').replace('）', ')').replace('：', ':')
    for non_ascii, ascii_digit in digit_map.items():
        text = text.replace(non_ascii, ascii_digit)
    return text

# Regex to extract English timestamp + text
timestamp_text_pattern = re.compile(r'\((\d+:\d{2})\)\s*(.*?)(?=\(\d+:\d{2}\)|$)', re.DOTALL)

language_data = {}
english_timestamps = []

# STEP 1: Load English transcript
with open(language_files['en'], 'r', encoding='utf-8') as f:
    english_content = normalize_text(f.read())
    english_lines = []
    for match in timestamp_text_pattern.finditer(english_content):
        timestamp = match.group(1)
        text = match.group(2).strip()
        english_timestamps.append(timestamp)
        english_lines.append(text)
    language_data['en'] = OrderedDict(zip(english_timestamps, english_lines))

# STEP 2: Load and clean other languages
def clean_line_start(line):
    line = line.strip()
    if line.startswith('(') and len(line) > 2 and line[1].isdigit():
        closing = line.find(')')
        if closing != -1:
            return line[closing+1:].strip()
    return line

for lang, filepath in language_files.items():
    if lang == 'en':
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_lines = [normalize_text(line.strip()) for line in f if line.strip()]
        cleaned_lines = [clean_line_start(line) for line in raw_lines]

    # Pad/truncate to match English timestamps
    if len(cleaned_lines) < len(english_timestamps):
        cleaned_lines += [''] * (len(english_timestamps) - len(cleaned_lines))
    else:
        cleaned_lines = cleaned_lines[:len(english_timestamps)]

    language_data[lang] = OrderedDict(zip(english_timestamps, cleaned_lines))

# STEP 3: Merge by English timestamps
merged_output = []

for timestamp in english_timestamps:
    block = {
        "start": timestamp,
        "text": {}
    }
    for lang in language_files:
        block["text"][lang] = language_data[lang].get(timestamp, "")
    merged_output.append(block)

# STEP 4: Save as JSON
with open('merged_subtitles_english_time.json', 'w', encoding='utf-8') as f:
    json.dump(merged_output, f, ensure_ascii=False, indent=2)

print(f"Merged {len(merged_output)} blocks based on English timestamps with line-order alignment and improved timestamp stripping.")
