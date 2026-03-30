import pandas as pd
from pathlib import Path

IN_PATH = Path("data/processed/healthcare_reviews_min20_labeled.csv")
OUT_PATH = Path("data/processed/healthcare_reviews_min20_aspects.csv")

ASPECT_KEYWORDS = {
    "aspect_doctor_care": [
        "doctor", "physician", "care", "treatment", "diagnosis", "diagnosed",
        "provider", "medical", "nurse practitioner", "specialist"
    ],
    "aspect_staff_behavior": [
        "staff", "front desk", "receptionist", "office staff", "nurse", "assistant",
        "rude", "friendly", "professional", "helpful", "attitude"
    ],
    "aspect_billing_cost": [
        "billing", "bill", "insurance", "cost", "price", "charged", "charge",
        "payment", "paid", "overcharged", "copay", "claim"
    ],
    "aspect_wait_time": [
        "wait", "waiting", "long time", "hours", "delayed", "delay", "appointment time",
        "late", "took forever", "on time"
    ],
    "aspect_communication": [
        "explained", "explain", "communication", "listen", "listened", "told",
        "answered", "questions", "informative", "clear", "unclear"
    ],
    "aspect_cleanliness_facility": [
        "clean", "dirty", "facility", "office", "room", "equipment", "hygiene",
        "sanitary", "organized", "waiting room"
    ],
}

def detect_aspect(text: str, keywords: list[str]) -> int:
    if not isinstance(text, str):
        return 0
    text = text.lower()
    return int(any(keyword in text for keyword in keywords))

def main():
    print("Loading labeled review dataset...")
    df = pd.read_csv(IN_PATH)

    print("Detecting aspects...")
    for aspect_col, keywords in ASPECT_KEYWORDS.items():
        df[aspect_col] = df["text_clean"].apply(lambda x: detect_aspect(x, keywords))

    df.to_csv(OUT_PATH, index=False)

    print("Saved:", OUT_PATH)
    print("\nAspect coverage summary:")
    for aspect_col in ASPECT_KEYWORDS.keys():
        print(f"{aspect_col}: {df[aspect_col].sum()} reviews")

if __name__ == "__main__":
    main()
