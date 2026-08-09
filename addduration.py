import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import yt_dlp

def get_duration(url):
    try:
        ydl_opts = {"quiet": True, "skip_download": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get("duration")
    except Exception as e:
        print(f"Failed for {url}: {e}")
        return None

def add_durations(input_file, output_file, max_workers=5):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    urls = [item.get("video") for item in data if item.get("video")]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(get_duration, url): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            duration = future.result()
            for item in data:
                if item.get("video") == url:
                    item["duration"] = duration

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Updated JSON written to {output_file}")

if __name__ == "__main__":
    add_durations("input.json", "output.json")
