import json
import re

# Files
JSON_FILE = "merged_subtitles_english_time.json"
TXT_FILE = "transcript-english.txt"

# Required language keys
REQUIRED_LANGS = ["en", "hi", "ta", "bn", "te", "mr", "fr", "es", "zh", "kn"]


def normalize_text(text):
    """Normalize text for safe comparison"""
    return re.sub(r"\s+", " ", text.strip())


def load_json():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_txt():
    transcript = {}
    pattern = re.compile(r"\((\d+:\d+)\)\s*(.*)")

    with open(TXT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            match = pattern.match(line.strip())
            if match:
                timestamp = match.group(1)
                text = match.group(2)
                transcript[timestamp] = normalize_text(text)

    return transcript


def main():
    print("🔍 Verifying subtitles...\n")

    json_data = load_json()
    transcript_data = load_txt()

    # Create lookup from JSON
    json_lookup = {}
    for block in json_data:
        start = block.get("start")
        json_lookup[start] = block

    all_ok = True

    # 1️⃣ Check timestamps & English match
    for timestamp, txt_english in transcript_data.items():
        if timestamp not in json_lookup:
            print(f"❌ Missing timestamp in JSON: {timestamp}")
            all_ok = False
            continue

        json_english = normalize_text(
            json_lookup[timestamp]["text"].get("en", "")
        )

        if txt_english != json_english:
            print(f"❌ English mismatch at {timestamp}")
            print(f"   TXT : {txt_english}")
            print(f"   JSON: {json_english}")
            all_ok = False

    # 2️⃣ Check all blocks have 10 language entries
    for block in json_data:
        start = block.get("start")
        text_dict = block.get("text", {})

        missing_langs = [
            lang for lang in REQUIRED_LANGS if lang not in text_dict
        ]

        if missing_langs:
            print(f"❌ Missing languages at {start}: {missing_langs}")
            all_ok = False

    # 3️⃣ Check for extra timestamps in JSON not in TXT
    for timestamp in json_lookup:
        if timestamp not in transcript_data:
            print(f"⚠️ Extra timestamp in JSON not in TXT: {timestamp}")

    print("\n----------------------------------")

    if all_ok:
        print("✅ All checks passed successfully!")
    else:
        print("❌ Some issues found. Please review above errors.")


if __name__ == "__main__":
    main()