import json

# Input and output file path
file_path = "input.json"

# Languages to move inside "text"
langs = ["en", "hi", "ta", "bn", "te", "mr", "fr", "es", "zh", "kn"]

# Read JSON list from file
with open(file_path, "r", encoding="utf-8") as f:
    data_list = json.load(f)

# Convert each item
converted_list = []

for item in data_list:
    new_item = {
        "start": item.get("start", ""),
        "text": {}
    }

    # Preserve other fields if needed
    for key, value in item.items():
        if key not in langs and key != "start":
            new_item[key] = value

    # Move languages into text object
    for lang in langs:
        new_item["text"][lang] = item.get(lang, "")

    converted_list.append(new_item)

# Overwrite same file
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(converted_list, f, ensure_ascii=False, indent=2)

print("Conversion completed successfully.")