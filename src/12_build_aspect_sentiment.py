import pandas as pd
from pathlib import Path

IN_PATH = Path("data/processed/healthcare_reviews_min20_aspects.csv")
OUT_PATH = Path("data/processed/healthcare_reviews_min20_aspect_sentiment.csv")

ASPECT_COLS = [
    "aspect_doctor_care",
    "aspect_staff_behavior",
    "aspect_billing_cost",
    "aspect_wait_time",
    "aspect_communication",
    "aspect_cleanliness_facility"
]

def main():
    print("Loading aspect review data...")
    df = pd.read_csv(IN_PATH)

    sentiment_map = {
        "positive": 1,
        "negative": -1,
        "neutral": 0
    }

    df["sentiment_score"] = df["sentiment"].map(sentiment_map).fillna(0)

    for col in ASPECT_COLS:
        new_col = col + "_sentiment"
        df[new_col] = df[col] * df["sentiment_score"]

    df.to_csv(OUT_PATH, index=False)
    print(f"Saved: {OUT_PATH}")

    print("\nCreated aspect sentiment columns:")
    for col in ASPECT_COLS:
        print("-", col + "_sentiment")

    print("\nPreview:")
    preview_cols = ["business_name", "sentiment"] + ASPECT_COLS + [c + "_sentiment" for c in ASPECT_COLS]
    print(df[preview_cols].head(5).to_string(index=False))

if __name__ == "__main__":
    main()
