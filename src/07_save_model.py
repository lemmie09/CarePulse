import pandas as pd
from pathlib import Path
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

IN_PATH = Path("data/processed/healthcare_reviews_min20_labeled.csv")
MODEL_DIR = Path("models")
VECTORIZER_PATH = MODEL_DIR / "tfidf_vectorizer.pkl"
MODEL_PATH = MODEL_DIR / "logreg_model.pkl"

def main():
    print("Loading data...")
    df = pd.read_csv(IN_PATH)

    # Binary classification for now
    df = df[df["sentiment"] != "neutral"].copy()

    X = df["text_clean"].astype(str)
    y = df["sentiment"].astype(str)

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
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

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    print("Saving vectorizer...")
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print("Saving model...")
    joblib.dump(model, MODEL_PATH)

    print("\nSaved files:")
    print(VECTORIZER_PATH)
    print(MODEL_PATH)

if __name__ == "__main__":
    main()
