import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

IN_PATH = Path("data/processed/healthcare_reviews_min20_labeled.csv")

def main():
    print("Loading data...")
    df = pd.read_csv(IN_PATH)

    # binary for clear explainability
    df = df[df["sentiment"] != "neutral"].copy()
    X = df["text_clean"].astype(str)
    y = df["sentiment"].astype(str)

    print("Train/test split...")
    X_train, _, y_train, _ = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Vectorizing...")
    vectorizer = TfidfVectorizer(
        max_features=20000,
        ngram_range=(1, 2),
        stop_words="english"
    )
    X_train_vec = vectorizer.fit_transform(X_train)

    print("Training model...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_vec, y_train)

    feature_names = vectorizer.get_feature_names_out()
    coef = model.coef_[0]  # for binary

    # sklearn orders classes alphabetically: ['negative', 'positive']
    # coef is for class 'positive' vs 'negative' (one-vs-rest style for binary)
    top_pos_idx = coef.argsort()[-20:][::-1]
    top_neg_idx = coef.argsort()[:20]

    print("\nTop Positive Features (push towards POSITIVE):")
    for i in top_pos_idx:
        print(f"{feature_names[i]:<25} {coef[i]:.4f}")

    print("\nTop Negative Features (push towards NEGATIVE):")
    for i in top_neg_idx:
        print(f"{feature_names[i]:<25} {coef[i]:.4f}")

if __name__ == "__main__":
    main()
