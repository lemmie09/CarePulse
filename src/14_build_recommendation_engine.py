import pandas as pd
from pathlib import Path

IN_PATH = Path("data/processed/provider_aspect_scores.csv")
OUT_PATH = Path("data/processed/provider_recommendation_scores.csv")

def normalize(series):
    return (series - series.min()) / (series.max() - series.min() + 1e-9)

def main():
    print("Loading provider data...")
    df = pd.read_csv(IN_PATH)

    # Normalize base features
    df["stars_norm"] = normalize(df["avg_stars"])
    df["sentiment_norm"] = df["positive_review_ratio"] / 100
    df["reviews_norm"] = normalize(df["total_reviews"])

    # Positive aspects
    df["positive_aspects"] = (
        df["doctor_care_score"] +
        df["staff_behavior_score"] +
        df["communication_score"] +
        df["cleanliness_facility_score"]
    ) / 4

    # Negative aspects (penalty)
    df["negative_penalty"] = (
        df["wait_time_score"].clip(lower=0) +
        df["billing_cost_score"].clip(lower=0)
    ) / 2

    # Final recommendation score
    df["recommendation_score"] = (
        0.30 * df["stars_norm"] +
        0.25 * df["sentiment_norm"] +
        0.15 * df["reviews_norm"] +
        0.20 * df["positive_aspects"] -
        0.10 * df["negative_penalty"]
    )

    df["recommendation_score"] = (df["recommendation_score"] * 100).round(2)

    df = df.sort_values(by="recommendation_score", ascending=False)

    df.to_csv(OUT_PATH, index=False)

    print(f"Saved: {OUT_PATH}")
    print("\nTop providers:")
    print(df[[
        "business_name",
        "city",
        "state",
        "recommendation_score",
        "avg_stars",
        "total_reviews"
    ]].head(10).to_string(index=False))


if __name__ == "__main__":
    main()
