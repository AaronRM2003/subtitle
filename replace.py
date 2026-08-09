import json

# === CONFIGURATION ===
INPUT_FILE = "merged_subtitles_english_time.json"     # Your input JSON file
OUTPUT_FILE = "merged_subtitles_english_time.json"   # Output JSON file

LANGUAGE = "hi"               # Language key to modify
OLD_WORD = "करार का सन्दूक"    # Word/sentence to replace
NEW_WORD = "वाचा का सन्दूक"    # Replacement text

# ======================

# Load JSON
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

replacement_count = 0

# Iterate through list
for item in data:
    if "text" in item and LANGUAGE in item["text"]:
        original_text = item["text"][LANGUAGE]

        if OLD_WORD in original_text:
            item["text"][LANGUAGE] = original_text.replace(OLD_WORD, NEW_WORD)
            replacement_count += 1

# Save updated JSON
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Done! Replaced {replacement_count} occurrence(s) in language '{LANGUAGE}'.")
print(f"Updated file saved as: {OUTPUT_FILE}")