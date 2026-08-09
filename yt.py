from pathlib import Path

eng = {f.stem for f in Path("yt_srt_output").glob("*.srt")}
orig = {f.stem for f in Path("yt_srt_output/original").glob("*.srt")}

print("English:", len(eng))
print("Original:", len(orig))
print("Intersection:", len(eng & orig))

print("\nMissing from original:")
for x in sorted(eng - orig):
    print(x)