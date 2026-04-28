import pandas as pd
from pathlib import Path

IN_PATH = Path("data/processed/provider_recommendation_scores.csv")
OUT_PATH = Path("data/processed/provider_peer_features.csv")

def percentile_rank(series):
    return series.rank(pct=True) * 100

def evidence_strength(n_reviews):
    if n_reviews >= 100:
        return "High"
    elif n_reviews >= 40:
        return "Medium"
    return "Low"

def main():
    print("Loading provider recommendation scores...")
    df = pd.read_csv(IN_PATH)

    # Core ranking percentile
    df["recommendation_percentile"] = percentile_rank(df["recommendation_score"]).round(2)

    # Evidence strength from review volume
    df["evidence_strength"] = df["total_reviews"].apply(evidence_strength)

    # Peer averages
    peer_avg = {
        "doctor_care_score": df["doctor_care_score"].mean(),
        "staff_behavior_score": df["staff_behavior_score"].mean(),
        "billing_cost_score": df["billing_cost_score"].mean(),
        "wait_time_score": df["wait_time_score"].mean(),
        "communication_score": df["communication_score"].mean(),
        "cleanliness_facility_score": df["cleanliness_facility_score"].mean(),
        "avg_stars": df["avg_stars"].mean(),
        "positive_review_ratio": df["positive_review_ratio"].mean(),
    }

    # Delta vs peer average
    df["doctor_vs_peer"] = (df["doctor_care_score"] - peer_avg["doctor_care_score"]).round(4)
    df["staff_vs_peer"] = (df["staff_behavior_score"] - peer_avg["staff_behavior_score"]).round(4)
    df["billing_vs_peer"] = (df["billing_cost_score"] - peer_avg["billing_cost_score"]).round(4)
    df["wait_vs_peer"] = (df["wait_time_score"] - peer_avg["wait_time_score"]).round(4)
    df["communication_vs_peer"] = (df["communication_score"] - peer_avg["communication_score"]).round(4)
    df["cleanliness_vs_peer"] = (df["cleanliness_facility_score"] - peer_avg["cleanliness_facility_score"]).round(4)
    df["stars_vs_peer"] = (df["avg_stars"] - peer_avg["avg_stars"]).round(4)
    df["positive_ratio_vs_peer"] = (df["positive_review_ratio"] - peer_avg["positive_review_ratio"]).round(4)

    df.to_csv(OUT_PATH, index=False)

    print(f"Saved: {OUT_PATH}")
    print("\nPreview:")
    print(df[[
        "business_name",
        "city",
        "state",
        "recommendation_score",
        "recommendation_percentile",
        "evidence_strength",
        "doctor_vs_peer",
        "communication_vs_peer",
        "wait_vs_peer",
        "billing_vs_peer"
    ]].head(10).to_string(index=False))

if __name__ == "__main__":
    main()
