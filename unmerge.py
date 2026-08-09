import json

# ---- SETTINGS ----
INPUT_FILE = "merged_subtitles_english_time.json"
OUTPUT_FILE = "output_clean.txt"
LANG = "en"    # change this to "hi", "ta", "ml", etc.
# -------------------

# Read JSON file
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

output_lines = []

# Process each item
for item in data:
    start = item.get("start", "")
    text_obj = item.get("text", {})
    text = text_obj.get(LANG, "(missing)")
    output_lines.append(f"({start}) {text}")

# Write to output file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print("✔ Done! Output saved in", OUTPUT_FILE)
