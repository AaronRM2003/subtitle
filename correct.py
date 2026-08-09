import json
import os

def replace_in_single_json_file(file_path, replacements):
    """
    Replaces words in ONE JSON file only.

    :param file_path: Full path to the JSON file
    :param replacements: Dictionary of {old_word: new_word}
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Skipping {file_path}: {e}")
        return

    def replace_in_obj(obj):
        if isinstance(obj, dict):
            return {k: replace_in_obj(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [replace_in_obj(elem) for elem in obj]
        elif isinstance(obj, str):
            for old_word, new_word in replacements.items():
                obj = obj.replace(old_word, new_word)
            return obj
        else:
            return obj

    updated_data = replace_in_obj(data)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=2)

    print(f"Updated: {file_path}")


def replace_in_json_files(folder_path, replacements):
    """
    Recursively replaces words in all JSON files of a folder and its subfolders.

    :param folder_path: Root folder of the project
    :param replacements: Dictionary of {old_word: new_word}
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if not file.endswith('.json'):
                continue

            file_path = os.path.join(root, file)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Skipping {file_path}: {e}")
                continue

            # Recursive replacement function
            def replace_in_obj(obj):
                if isinstance(obj, dict):
                    return {k: replace_in_obj(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [replace_in_obj(elem) for elem in obj]
                elif isinstance(obj, str):
                    for old_word, new_word in replacements.items():
                        obj = obj.replace(old_word, new_word)
                    return obj
                else:
                    return obj

            updated_data = replace_in_obj(data)

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(updated_data, f, ensure_ascii=False, indent=2)

            print(f"Updated: {file_path}")


# Example usage:
folder = "C:\\Users\\mincy\\Desktop\\kreupasanam\\my-testimonies-site\\public"
file_path = "merged_subtitles_english_time.json"


replacements_dict = {
    "अल्लाह": "ईश्वर",
"ख़ुदा": "ईश्वर",
"रब": "प्रभु",
"ईमान": "विश्वास",
"मोमिन": "विश्वासी",
"इंजील": "सुसमाचार",
"आयत": "वचन",
"पुजारी": "पुरोहित",
"पंडित": "धर्मगुरु",
"साधु": "संन्यासी",
"पूजा": "आराधना",
"पूजन": "आराधना",
"मंदिर": "कलीसिया",
"देवालय": "कलीसिया",
"दीक्षा": "अभिषेक",
"संस्कार": "संस्कार (साक्रामेंट)",

"యెహోవా": "ప్రభువు",
"పూజారి": "పాద్రి",
"పూజ": "ఆరాధన",
"ఆలయం": "చర్చి",
"దేవాలయం": "చర్చి",

"ಯೆಹೋವ": "ಕರ್ತನು",
"ಪೂಜಾರಿ": "ಯಾಜಕ",
"ಪೂಜೆ": "ಆರಾಧನೆ",
"ದೇವಾಲಯ": "ಚರ್ಚ್",

"আল্লাহ": "ঈশ্বর",
"খোদা": "ঈশ্বর",
"পূজারি": "যাজক",
"পুরোহিত": "যাজক",
"নামাজ": "প্রার্থনা",
"দোয়া": "প্রার্থনা",
"মন্দির": "গির্জা",

"上帝": "天主",
"圣灵": "圣神",
"教会": "圣教会",
"福音": "圣福音",
"祭司": "司铎",

}
# replace_in_json_files(folder, replacements_dict)
replace_in_single_json_file(file_path, replacements_dict)

