import requests
import time

API_KEY = "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"
INPUT_FILE = "output_clean.txt"
OUTPUT_FILE = "transcript-english.txt"

def translate_malayalam_to_english(text):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",  # try "meta-llama/llama-3-8b-instruct" if needed
        "messages": [
            {"role": "system", "content": "You are a professional human translator. Translate Malayalam text into fluent, natural English."},
            {"role": "user", "content": text}
        ],
        "temperature": 0.2
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()

def main():
    # Read all Malayalam lines
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Open output file for writing translations
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for i in range(0, len(lines), 5):
            chunk = lines[i:i+5]
            text_block = "\n".join(chunk)

            print(f"Translating lines {i+1}-{i+len(chunk)}...")

            try:
                english_translation = translate_malayalam_to_english(text_block)
            except Exception as e:
                print("Error:", e)
                english_translation = "[Error translating this block]"

            # Save to output file
            out.write(f"\n--- Lines {i+1}-{i+len(chunk)} ---\n")
            out.write(english_translation + "\n")

            # Small delay to avoid rate limits
            time.sleep(1)

    print(f" All translations saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
