import pandas as pd
from pathlib import Path

IN_PATH = Path("data/processed/healthcare_businesses.csv")
OUT_PATH = Path("data/processed/healthcare_businesses_min20.csv")

def main():
    df = pd.read_csv(IN_PATH)
    df2 = df[df["review_count"] >= 20].copy()
    df2.to_csv(OUT_PATH, index=False)
    print("Saved:", OUT_PATH)
    print("Businesses (all):", len(df))
    print("Businesses (>=20 reviews):", len(df2))
    print(df2.head(5).to_string(index=False))

if __name__ == "__main__":
    main()
