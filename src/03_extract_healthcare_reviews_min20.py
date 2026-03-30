import json
import pandas as pd
from pathlib import Path

BIZ_PATH = Path("data/processed/healthcare_businesses_min20.csv")
REVIEW_PATH = Path("data/raw/yelp_academic_dataset_review.json")
OUT_PATH = Path("data/processed/healthcare_reviews_min20.csv")

def main():
    # Load healthcare business ids
    biz = pd.read_csv(BIZ_PATH, usecols=["business_id", "name", "city", "state", "latitude", "longitude"])
    biz_ids = set(biz["business_id"].astype(str).tolist())
    biz_map = biz.set_index("business_id").to_dict(orient="index")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    kept = 0
    scanned = 0

    with REVIEW_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            scanned += 1
            r = json.loads(line)
            bid = r.get("business_id")
            if bid in biz_ids:
                binfo = biz_map[bid]
                rows.append({
                    "business_id": bid,
                    "business_name": binfo["name"],
                    "city": binfo["city"],
                    "state": binfo["state"],
                    "latitude": binfo["latitude"],
                    "longitude": binfo["longitude"],
                    "review_id": r.get("review_id"),
                    "stars": r.get("stars"),
                    "date": r.get("date"),
                    "text": r.get("text", "")
                })
                kept += 1

            # progress print every 500k lines
            if scanned % 500000 == 0:
                print(f"Scanned {scanned:,} lines | Kept {kept:,} reviews")

    df = pd.DataFrame(rows)
    df.to_csv(OUT_PATH, index=False)

    print("Saved:", OUT_PATH)
    print("Total kept reviews:", len(df))
    print(df.head(3).to_string(index=False))

if __name__ == "__main__":
    main()
