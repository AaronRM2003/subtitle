import os
import json
import shutil
from datetime import datetime

FOLDER = r"C:\Users\mincy\Desktop\kreupasanam\my-testimonies-site\public"

def backup_file(path):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{path}.bak_{ts}"
    shutil.copy2(path, backup_path)

def fix_eglise_in_en(obj, changes, file_path):
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            if k == "en" and isinstance(v, str):
                original = v
                fixed = (
                    v.replace("liturgia", "ritual")
                )
                if fixed != original:
                    changes.append((file_path, original, fixed))
                new_obj[k] = fixed
            else:
                new_obj[k] = fix_eglise_in_en(v, changes, file_path)
        return new_obj

    elif isinstance(obj, list):
        return [fix_eglise_in_en(e, changes, file_path) for e in obj]

    else:
        return obj

def process_folder(folder):
    total_files = 0
    modified_files = 0
    changes = []

    for root, _, files in os.walk(folder):
        for file in files:
            if not file.lower().endswith(".json"):
                continue

            path = os.path.join(root, file)
            total_files += 1

            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"❌ Skipping {path}: {e}")
                continue

            new_data = fix_eglise_in_en(data, changes, path)

            if new_data != data:
                backup_file(path)
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(new_data, f, ensure_ascii=False, indent=2)
                modified_files += 1

    print("\n===== SUMMARY =====")
    print(f"JSON files scanned : {total_files}")
    print(f"Files modified     : {modified_files}")
    print(f"Total replacements : {len(changes)}")

    if changes:
        print("\nSample changes:")
        for fp, before, after in changes[:5]:
            print(f"- {fp}")
            print(f"  BEFORE: {before}")
            print(f"  AFTER : {after}")

    print("\n✅ Done.")

if __name__ == "__main__":
    process_folder(FOLDER)