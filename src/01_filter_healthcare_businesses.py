import json
import pandas as pd
from pathlib import Path

BUSINESS_PATH = Path("data/raw/yelp_academic_dataset_business.json")
OUT_PATH = Path("data/processed/healthcare_businesses.csv")

# Human healthcare keywords (whitelist)
INCLUDE = [
    "Health & Medical", "Doctors", "Dentists", "Hospitals", "Urgent Care",
    "Medical Centers", "Clinics", "Physical Therapy", "Optometrists",
    "Psychiatrists", "Counseling", "Therapists", "Chiropractors"
]

# Exclusions to avoid common false positives
EXCLUDE = [
    "Veterinarians", "Pet", "Pets"
]

def is_healthcare(categories: str) -> bool:
    if not categories:
        return False
    if any(x in categories for x in EXCLUDE):
        return False
    return any(x in categories for x in INCLUDE)

def main():
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    with BUSINESS_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            b = json.loads(line)
            cats = b.get("categories") or ""
            if is_healthcare(cats):
                rows.append({
                    "business_id": b["business_id"],
                    "name": b.get("name"),
                    "city": b.get("city"),
                    "state": b.get("state"),
                    "latitude": b.get("latitude"),
                    "longitude": b.get("longitude"),
                    "stars": b.get("stars"),
                    "review_count": b.get("review_count"),
                    "categories": cats
                })

    df = pd.DataFrame(rows)
    df.to_csv(OUT_PATH, index=False)

    print("Saved:", OUT_PATH)
    print("Healthcare businesses:", len(df))
    print(df.head(5).to_string(index=False))

if __name__ == "__main__":
    main()
