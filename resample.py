import os
import argparse
import soundfile as sf
import numpy as np
import torch
import torchaudio
from scipy.fft import rfft, rfftfreq
from tqdm import tqdm

SOURCE_DIR = "Result"
OUTPUT_DIR = "resample"

def get_all_wav_files(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(".wav")]

def estimate_max_frequency(data, sr, threshold=0.001):
    if len(data.shape) > 1:
        data = data[:, 0]
    N = len(data)
    spectrum = np.abs(rfft(data))
    spectrum = spectrum / np.max(spectrum)
    freqs = rfftfreq(N, 1 / sr)

    for i in range(len(freqs)-1, -1, -1):
        if spectrum[i] > threshold:
            return freqs[i]
    return sr / 2

def choose_target_sr(max_freq):
    if max_freq <= 4000:
        return 8000
    elif max_freq <= 8000:
        return 16000
    elif max_freq <= 22000:
        return 44100
    elif max_freq <= 24000:
        return 48000
    else:
        return 96000

def resample_torch(data, orig_sr, target_sr):
    if orig_sr == target_sr:
        return data
    waveform = torch.from_numpy(data.T).float()  # (channels, time)
    resampler = torchaudio.transforms.Resample(orig_sr, target_sr)
    resampled = resampler(waveform).numpy().T  # (time, channels)
    return resampled

def process_file(path, output_dir):
    try:
        data, sr = sf.read(path)
        max_freq = estimate_max_frequency(data, sr)
        target_sr = choose_target_sr(max_freq)

        resampled = resample_torch(data, sr, target_sr)

        filename = os.path.basename(path)
        out_name = "re_" + filename
        out_path = os.path.join(output_dir, out_name)

        sf.write(out_path, resampled, target_sr)
    except Exception as e:
        print(f"Error processing {path}: {e}")

def parse_args():
    parser = argparse.ArgumentParser(description="Resample AudioSet clips by label.")
    parser.add_argument("--label", type=str, nargs='+', required=True, help="One or more label names")
    parser.add_argument("--num", required=True, help="Number of samples per label or 'all'")
    return parser.parse_args()

def filter_files_by_labels(files, labels):
    filtered = []
    labels = [label.lower().replace(" ", "_") for label in labels]
    for label in labels:
        for f in files:
            if label in f.lower():
                filtered.append(f)
    return filtered

def main():
    args = parse_args()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_files = get_all_wav_files(SOURCE_DIR)
    all_filenames = [os.path.basename(f) for f in all_files]

    filtered_files = filter_files_by_labels(all_filenames, args.label)

    if not filtered_files:
        print("No matching wav files found for given labels.")
        return

    selected_files = filtered_files if args.num.lower() == "all" else filtered_files[:int(args.num)]
    selected_paths = [os.path.join(SOURCE_DIR, f) for f in selected_files]

    for path in tqdm(selected_paths, desc="Resampling", ncols=100):
        process_file(path, OUTPUT_DIR)

    print(f"Completed resampling {len(selected_paths)} files.")

if __name__ == "__main__":
    main()
