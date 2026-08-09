from pathlib import Path


def sbv_time_to_srt(time_str):
    """
    Converts:
    0:00:06.000 -> 00:00:06,000
    """
    h, m, s = time_str.split(":")
    sec, ms = s.split(".")
    return f"{int(h):02d}:{int(m):02d}:{int(sec):02d},{ms}"


def convert_sbv_to_srt(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]

    srt = []
    index = 1
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Timestamp line
        if "," in line and ":" in line:
            start, end = line.split(",")

            start = sbv_time_to_srt(start)
            end = sbv_time_to_srt(end)

            i += 1
            text_lines = []

            while i < len(lines) and lines[i].strip():
                text_lines.append(lines[i])
                i += 1

            srt.append(str(index))
            srt.append(f"{start} --> {end}")
            srt.extend(text_lines)
            srt.append("")

            index += 1

        i += 1

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(srt))

    print(f"Saved {output_file}")


if __name__ == "__main__":
    input_file = "input.sbv"
    output_file = "output.srt"

    convert_sbv_to_srt(input_file, output_file)