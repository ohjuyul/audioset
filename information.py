import os
import csv
import soundfile as sf

SOURCE_DIR = "resample"
CSV_PATH = r"C:./information/result_info.csv"

def extract_label_from_filename(filename):
    name = os.path.splitext(filename)[0]
    if name.startswith("re_"):
        name = name[3:]
    label_parts = name.split("_")[:-1]
    return " ".join(label_parts)

def process_file(path):
    try:
        data, sr = sf.read(path)
        duration = len(data) / sr
        return os.path.abspath(path), extract_label_from_filename(os.path.basename(path)), duration, sr
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return None

def main():
    wav_files = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith(".wav")]
    if not wav_files:
        print("No .wav files found in resample/")
        return

    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)

    with open(CSV_PATH, mode='w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["File Path", "Label", "Seconds", "Sample Rate"])

        for filename in wav_files:
            full_path = os.path.join(SOURCE_DIR, filename)
            info = process_file(full_path)
            if info:
                path, label, duration, sr = info
                writer.writerow([path, label, f"{duration:.2f}", sr])

    print(f"CSV saved to {CSV_PATH}")

if __name__ == "__main__":
    main()
