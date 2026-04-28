import pandas as pd
from pathlib import Path

IN_PATH = Path("data/processed/healthcare_reviews_min20_aspect_sentiment.csv")
OUT_PATH = Path("data/processed/provider_aspect_scores.csv")

ASPECT_SCORE_MAP = {
    "aspect_doctor_care_sentiment": "doctor_care_score",
    "aspect_staff_behavior_sentiment": "staff_behavior_score",
    "aspect_billing_cost_sentiment": "billing_cost_score",
    "aspect_wait_time_sentiment": "wait_time_score",
    "aspect_communication_sentiment": "communication_score",
    "aspect_cleanliness_facility_sentiment": "cleanliness_facility_score",
}

def safe_mean(series):
    return round(series.mean(), 4) if len(series) > 0 else 0.0

def main():
    print("Loading review-level aspect sentiment data...")
    df = pd.read_csv(IN_PATH)

    group_cols = ["business_name", "city", "state"]

    agg_dict = {
        "review_id": "count",
        "stars": "mean",
        "sentiment": lambda x: (x == "positive").mean()
    }

    for src_col in ASPECT_SCORE_MAP.keys():
        agg_dict[src_col] = safe_mean

    provider_df = df.groupby(group_cols).agg(agg_dict).reset_index()

    provider_df = provider_df.rename(columns={
        "review_id": "total_reviews",
        "stars": "avg_stars",
        "sentiment": "positive_review_ratio"
    })

    for src_col, dst_col in ASPECT_SCORE_MAP.items():
        provider_df = provider_df.rename(columns={src_col: dst_col})

    provider_df["avg_stars"] = provider_df["avg_stars"].round(2)
    provider_df["positive_review_ratio"] = (provider_df["positive_review_ratio"] * 100).round(2)

    provider_df.to_csv(OUT_PATH, index=False)

    print(f"Saved: {OUT_PATH}")
    print("\nPreview:")
    print(provider_df.head(10).to_string(index=False))

if __name__ == "__main__":
    main()
