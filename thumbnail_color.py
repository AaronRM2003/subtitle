import json
import requests
from io import BytesIO
from PIL import Image
from collections import Counter

def get_youtube_thumbnail_url(video_url: str):
    if "youtu.be/" in video_url:
        video_id = video_url.split("youtu.be/")[1].split("?")[0]
    elif "youtube.com/watch?v=" in video_url:
        video_id = video_url.split("v=")[1].split("&")[0]
    else:
        return None
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"


def get_dominant_color(image):
    image = image.resize((200, 200))
    image = image.convert("RGB")

    pixels = list(image.getdata())

    # Remove white/near-white pixels
    filtered = [
        (r, g, b)
        for (r, g, b) in pixels
        if not (r > 220 and g > 220 and b > 220)
    ]

    # fallback if image mostly white
    if len(filtered) < 10:
        filtered = pixels

    # Count occurrences
    color_counts = Counter(filtered)
    dominant = color_counts.most_common(1)[0][0]

    return "#{:02x}{:02x}{:02x}".format(*dominant)


def process_json(input_file: str, output_file: str):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        video_url = item.get("video")
        if not video_url:
            continue

        thumbnail_url = get_youtube_thumbnail_url(video_url)

        try:
            response = requests.get(thumbnail_url, timeout=10)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))

            color = get_dominant_color(img)
            item["color"] = color

        except Exception as e:
            print("Error:", e)
            item["color"] = None

    with open(output_file, "w", encoding="utf-8") as out:
        json.dump(data, out, indent=2, ensure_ascii=False)

    print("Done →", output_file)


if __name__ == "__main__":
    process_json("test.json", "output.json")
