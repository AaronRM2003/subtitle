import os
from docx import Document

# Base folder where your Word (.docx) files are stored
base_path = "C:/Users/mincy/Downloads/"

# Map of language codes to filenames
language_files = {
    'english': 'daily_bread.docx',
    'hindi': 'daily_bread (4).docx',
    'telugu': 'daily_bread (9).docx',
    'tamil': 'daily_bread (8).docx',
    'kannada': 'daily_bread (5).docx',
    'bengali': 'daily_bread (1).docx',
    'chinese': 'daily_bread (2).docx',
    'french': 'daily_bread (3).docx',
    'spanish': 'daily_bread (7).docx',
    'marathi': 'daily_bread (6).docx',
}

# Output filename format
def get_output_filename(lang_code, episode_number):
    return f"transcript-{lang_code}.txt"

# Extract episodes from a .docx file
def extract_episodes_from_docx(filepath):
    doc = Document(filepath)
    episodes = []
    current_episode = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if text == "":
            if current_episode:
                episodes.append(current_episode)
                current_episode = []
        else:
            current_episode.append(text)

    if current_episode:
        episodes.append(current_episode)

    return episodes

# Save episode content to a text file
def save_episode_to_file(episode_lines, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(episode_lines))
    print("Saved:", output_path)

# Ask which episode to extract
episode_input = input("Enter the episode number to extract (e.g., 1, 2, 3...): ")
try:
    episode_index = int(episode_input) - 1
    if episode_index < 0:
        raise ValueError
except ValueError:
    print("Invalid input. Must be a positive integer.")
    exit()

# Process each language file
for lang_code, filename in language_files.items():
    filepath = os.path.join(base_path, filename)
    if not os.path.exists(filepath):
        print("File not found:", filepath)
        continue

    episodes = extract_episodes_from_docx(filepath)

    if episode_index >= len(episodes):
        print(f"Episode {episode_index + 1} not found in {filename} (only {len(episodes)} episodes found).")
        continue

    output_filename = get_output_filename(lang_code, episode_index + 1)
    save_episode_to_file(episodes[episode_index], output_filename)
