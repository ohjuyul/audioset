import os
import soundfile as sf
import numpy as np
from scipy.signal import resample_poly
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

def resample_audio(data, orig_sr, target_sr):
    if orig_sr == target_sr:
        return data
    gcd = np.gcd(orig_sr, target_sr)
    up = target_sr // gcd
    down = orig_sr // gcd
    return resample_poly(data, up, down, axis=0)

def process_file(path, output_dir):
    try:
        data, sr = sf.read(path)
        max_freq = estimate_max_frequency(data, sr)
        new_sr = int(np.ceil(max_freq * 2))

        resampled = resample_audio(data, sr, new_sr)

        filename = os.path.basename(path)
        out_name = "re_" + filename
        out_path = os.path.join(output_dir, out_name)

        sf.write(out_path, resampled, new_sr)
    except Exception as e:
        print(f"Error processing {path}: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    files = get_all_wav_files(SOURCE_DIR)

    if not files:
        print("Result/ 폴더에 .wav 파일이 없습니다.")
        return

    for path in tqdm(files, desc="Resampling", ncols=100):
        process_file(path, OUTPUT_DIR)

    print(f"complete")

if __name__ == "__main__":
    main()
