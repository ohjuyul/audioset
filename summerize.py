import pandas as pd

CSV_PATH = r"./information/result_info.csv"
SUMMARY_PATH = r"./information/sum.csv"

def main():
    df = pd.read_csv(CSV_PATH)

    df["Seconds"] = pd.to_numeric(df["Seconds"], errors='coerce')

    label_stats = df.groupby("Label")["Seconds"].agg(
        Count="count",
        Mean="mean",
        Variance="var",
        Max="max",
        Min="min"
    ).reset_index()

    total_stats = df["Seconds"].agg(
        Count="count",
        Mean="mean",
        Variance="var",
        Max="max",
        Min="min"
    ).to_frame().T
    total_stats.insert(0, "Label", "전체")

    final_df = pd.concat([label_stats, total_stats], ignore_index=True)

    print("라벨별 오디오 길이 통계:\n")
    print(final_df.to_string(index=False))

    final_df.to_csv(SUMMARY_PATH, index=False, encoding="utf-8-sig")
    print(f"\n통계 저장 완료: {SUMMARY_PATH}")

if __name__ == "__main__":
    main()
