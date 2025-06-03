import argparse
import subprocess
import os
import soundfile as sf
import random
import json
from tqdm import tqdm

URL = "https://www.youtube.com/watch?v="
FULL_DIR = "full"
TRIM_DIR = "Result"
ONTOLOGY_PATH = r"./ontology.json"
DATA_FILE = "data.txt"

def load_label_name_to_id(path):
    with open(path, "r", encoding="utf-8") as f:
        ontology = json.load(f)
    return {item["name"].lower(): item["id"] for item in ontology}

def download_audio(video_id, output_path):
    if os.path.exists(output_path):
        return
    cmd = [
        "yt-dlp",
        URL + video_id,
        "--extract-audio",
        "--audio-format", "wav",
        "--audio-quality", "0",
        "-o", output_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def trim_audio(input_path, start_sec, end_sec, output_path):
    cmd = [
        "ffmpeg",
        "-ss", str(start_sec),
        "-to", str(end_sec),
        "-i", input_path,
        "-ac", "1",
        "-ar", "48000",
        "-y",
        output_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def get_next_index(folder, prefix):
    existing = [f for f in os.listdir(folder) if f.startswith(prefix + "_") and f.endswith(".wav")]
    indices = []
    for f in existing:
        try:
            idx = int(f[len(prefix)+1:-4])
            indices.append(idx)
        except:
            pass
    return max(indices)+1 if indices else 0

def process_line(line, label_name):
    parts = line.strip().split(',', 3)
    if len(parts) < 4:
        return False

    video_id, start_str, end_str, _ = parts
    video_id = video_id.strip()
    try:
        start_sec = float(start_str.strip())
        end_sec = float(end_str.strip())
    except ValueError:
        return False

    safe_prefix = label_name.replace(" ", "_")
    idx = get_next_index(TRIM_DIR, safe_prefix)

    full_audio_path = os.path.join(FULL_DIR, f"full_{safe_prefix}_{idx}.wav")
    trimmed_audio_path = os.path.join(TRIM_DIR, f"{safe_prefix}_{idx}.wav")

    try:
        download_audio(video_id, full_audio_path)
        trim_audio(full_audio_path, start_sec, end_sec, trimmed_audio_path)
        return True
    except Exception as e:
        print(f"[{label_name}] Error: {e}")
        return False

def run_label(label_id, label_name, num_arg):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        matching_lines = [line for line in f if label_id in line]

    if not matching_lines:
        print(f"No matching lines found for label ID: {label_id}")
        return 0, 0, label_name

    if num_arg == "all":
        sampled_lines = matching_lines
    else:
        num = int(num_arg)
        sampled_lines = matching_lines[:num]

    success, fail = 0, 0
    for line in tqdm(sampled_lines, desc=f"{label_name}", ncols=100):
        if process_line(line, label_name):
            success += 1
        else:
            fail += 1

    return success, fail, label_name

def parse_args():
    parser = argparse.ArgumentParser(description="Download and segment AudioSet clips by label.")
    parser.add_argument("--label", type=str, nargs='+', required=True,
                        help='One or more label names (e.g. "Fire alarm" "Explosion") or "all"')
    parser.add_argument("--num", required=True,
                        help='Number of samples to extract per label or "all"')
    parser.add_argument("--exclude", nargs='*', default=[],
                        help='Label names to exclude (e.g. "Speech")')
    return parser.parse_args()

def main():
    os.makedirs(FULL_DIR, exist_ok=True)
    os.makedirs(TRIM_DIR, exist_ok=True)

    args = parse_args()
    label_inputs = [label.strip().lower() for label in args.label]
    num_arg = args.num.strip().lower()
    exclude_list = [name.lower() for name in args.exclude]

    name_to_id = load_label_name_to_id(ONTOLOGY_PATH)
    results = []

    if len(label_inputs) == 1 and label_inputs[0] == "all":
        for name, id_ in name_to_id.items():
            if name.lower() in exclude_list:
                continue
            suc, fail, label_name = run_label(id_, name, num_arg)
            results.append((label_name, suc, fail))
    else:
        for label_name_input in label_inputs:
            if label_name_input not in name_to_id:
                print(f"Label '{label_name_input}' not found in ontology.")
                continue
            label_id = name_to_id[label_name_input]
            suc, fail, label_name = run_label(label_id, label_name_input, num_arg)
            results.append((label_name, suc, fail))

    with open("last.txt", "w", encoding="utf-8") as f:
        for label_name, suc, fail in results:
            f.write(f"{label_name}  suc: {suc}  fail: {fail}\n")

if __name__ == "__main__":
    main()
