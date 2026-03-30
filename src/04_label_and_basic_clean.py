import pandas as pd
import re
from pathlib import Path

IN_PATH = Path("data/processed/healthcare_reviews_min20.csv")
OUT_PATH = Path("data/processed/healthcare_reviews_min20_labeled.csv")

def label_from_stars(stars: float) -> str:
    if stars <= 2:
        return "negative"
    if stars == 3:
        return "neutral"
    return "positive"

def basic_clean(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.replace("\n", " ").replace("\t", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text

def main():
    df = pd.read_csv(IN_PATH)

    df["sentiment"] = df["stars"].apply(label_from_stars)
    df["text_clean"] = df["text"].apply(basic_clean)

    df = df[df["text_clean"].str.len() > 0].copy()

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    print("Saved:", OUT_PATH)
    print("Total rows:", len(df))
    print("Sentiment Distribution:")
    print(df["sentiment"].value_counts())

if __name__ == "__main__":
    main()
