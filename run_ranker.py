import argparse
import pandas as pd
from src.subject_ranker import rank_subjects


def main():
    parser = argparse.ArgumentParser(description="Rank email subject lines using Wilson lower bound.")
    parser.add_argument("--input", required=True, help="Path to input CSV (must include subject, sendings, opens).")
    parser.add_argument("--min-sendings", type=int, default=50, help="Minimum sendings threshold (default: 50).")
    parser.add_argument("--output", default="outputs/wilson_ranked.csv", help="Output CSV path.")
    parser.add_argument("--top", type=int, default=30, help="Also save top N to outputs/top_email_subjects_wilson.csv")

    args = parser.parse_args()

    df = pd.read_csv(args.input)

    # Basic column normalization (optional but helpful)
    df.columns = [c.strip().lower() for c in df.columns]

    ranked = rank_subjects(df, min_sendings=args.min_sendings)

    # Ensure output folder exists
    import os
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)

    ranked.to_csv(args.output, index=False)

    top_path = "outputs/top_email_subjects_wilson.csv"
    os.makedirs("outputs", exist_ok=True)
    ranked.head(args.top).to_csv(top_path, index=False)

    print("✅ Done")
    print(f"- Ranked rows: {len(ranked)}")
    print(f"- Saved ranked file: {args.output}")
    print(f"- Saved top {args.top}: {top_path}")
    print("\nTop 5 preview:")
    print(ranked[['subject', 'total_sendings', 'open_rate', 'wilson_score']].head(5).to_string(index=False))


if __name__ == "__main__":
    main()

