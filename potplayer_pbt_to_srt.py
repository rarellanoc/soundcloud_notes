import sys
import os

def convert_pbt_to_srt(input_path, output_path=None, read_time=2.0, separator=','):
    if output_path is None:
        base, _ = os.path.splitext(input_path)
        output_path = base + ".srt"

    with open(input_path, 'r', encoding='utf-8') as infile:
        lines = [line.strip() for line in infile if line.strip()]

    srt_entries = []
    for idx, line in enumerate(lines, 1):
        try:
            timestamp, text = line.split(separator, 1)
        except ValueError:
            print(f"Skipping line {idx}: missing separator '{separator}': {line}")
            continue

        # Convert timestamp (assumed in seconds or H:MM:SS.MS or MM:SS.MS) to SRT format
        start_sec = parse_timestamp_to_seconds(timestamp.strip())
        end_sec = start_sec + read_time

        start_srt = seconds_to_srt_timestamp(start_sec)
        end_srt = seconds_to_srt_timestamp(end_sec)

        srt_entries.append(f"{idx}\n{start_srt} --> {end_srt}\n{text.strip()}\n")

    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.writelines(srt_entries)

    print(f"Converted {input_path} to {output_path}")

def parse_timestamp_to_seconds(ts):
    # Accepts: "10", "1:23", "1:02:03", "1:23.45", "1:02:03.456"
    ts = ts.replace(',', '.')
    parts = ts.split(':')
    if len(parts) == 1:
        # seconds
        return float(parts[0])
    elif len(parts) == 2:
        # MM:SS
        m, s = parts
        return int(m) * 60 + float(s)
    elif len(parts) == 3:
        # HH:MM:SS
        h, m, s = parts
        return int(h) * 3600 + int(m) * 60 + float(s)
    else:
        raise ValueError(f"Invalid timestamp format: {ts}")

def seconds_to_srt_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python potplayer_pbt_to_srt.py input.pbt [output.srt]")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    convert_pbt_to_srt(input_file, output_file)