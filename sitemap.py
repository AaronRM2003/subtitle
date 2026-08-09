import json
import re

# Configuration
site_origin = "https://kreupasanamtestimonies.com"
json_file_path = "C:\\Users\\mincy\\Desktop\\kreupasanam\\my-testimonies-site\\public\\assets\\dhyanam-content.json"  # path to your JSON file
content_type = "dhyanam"  # type for URL path

# Slugify function
def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"\s+", "-", text)          # spaces → hyphens
    text = re.sub(r"[^\w\-]+", "", text)      # remove non-word chars
    text = re.sub(r"\-\-+", "-", text)        # collapse multiple hyphens
    return text

# Load JSON
with open(json_file_path, encoding="utf-8") as f:
    data = json.load(f)

# Generate URLs for English only
urls = []
for item in data:
    item_id = item.get("id")
    title = item.get("title", {}).get("en")
    if title:
        slug = slugify(title)
        slug = slug.replace("/", "")  # optional: remove slashes
        full_url = f"{site_origin}/en/{content_type}/{item_id}-{slug}"
        urls.append(full_url)

# Output
for url in urls:
    print("<url><loc>"+url.encode("utf-8").decode("utf-8")+"</loc></url>")
