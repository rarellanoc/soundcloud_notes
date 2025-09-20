import sys
import os

def convert_dual_pbt_to_srt(
    input_path1,
    input_path2,
    output_path=None,
    read_time=2.0,
    separator=',',
    left_prefix='1',
    right_prefix='2',
    placeholder='----'
):
    if output_path is None:
        base, _ = os.path.splitext(input_path1)
        output_path = base + "_dual.srt"

    # Read and parse both input files
    entries1 = parse_pbt_entries(input_path1, separator, left_prefix)
    entries2 = parse_pbt_entries(input_path2, separator, right_prefix)

    # Merge all unique timestamps, keeping track of which text belongs to which.
    all_times = set([e[0] for e in entries1] + [e[0] for e in entries2])
    all_times = sorted(all_times)

    # Build dictionaries for fast lookup
    dict1 = {e[0]: e[1] for e in entries1}
    dict2 = {e[0]: e[1] for e in entries2}

    srt_entries = []
    idx = 1
    for t in all_times:
        text1 = dict1.get(t, placeholder)
        text2 = dict2.get(t, placeholder)

        # Visually distinguish both lines, align 1 left and 2 right.
        if text1 != placeholder and text2 != placeholder:
            # Both present at the same timestamp, add a visual separator
            srt_text = f"{text1.ljust(40)} || {text2.rjust(40)}"
        else:
            srt_text = f"{text1.ljust(40)}    {text2.rjust(40)}"

        start_sec = parse_timestamp_to_seconds(t)
        end_sec = start_sec + read_time
        start_srt = seconds_to_srt_timestamp(start_sec)
        end_srt = seconds_to_srt_timestamp(end_sec)

        srt_entries.append(f"{idx}\n{start_srt} --> {end_srt}\n{srt_text}\n\n")
        idx += 1

    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.writelines(srt_entries)

    print(f"Converted {input_path1} and {input_path2} to {output_path}")

def parse_pbt_entries(input_path, separator, prefix):
    entries = []
    with open(input_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            try:
                timestamp, text = line.split(separator, 1)
                # Prepend prefix if not already present
                text = text.strip()
                if not text.startswith(prefix):
                    text = f"{prefix}: {text}"
                entries.append((timestamp.strip(), text))
            except ValueError:
                # Skip malformed lines
                continue
    return entries

def parse_timestamp_to_seconds(ts):
    # Accepts: "10", "1:23", "1:02:03", "1:23.45", "1:02:03.456"
    ts = ts.replace(',', '.')
    parts = ts.split(':')
    if len(parts) == 1:
        return float(parts[0])
    elif len(parts) == 2:
        m, s = parts
        return int(m) * 60 + float(s)
    elif len(parts) == 3:
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
    if len(sys.argv) < 3:
        print("Usage: python potplayer_pbt_dual_to_srt.py input1.pbt input2.pbt [output.srt]")
        sys.exit(1)
    input_file1 = sys.argv[1]
    input_file2 = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else None
    convert_dual_pbt_to_srt(input_file1, input_file2, output_file)