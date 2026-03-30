import joblib
from pathlib import Path

MODEL_PATH = Path("models/logreg_model.pkl")
VECTORIZER_PATH = Path("models/tfidf_vectorizer.pkl")

def main():
    print("Loading saved model and vectorizer...")
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

    review = input("\nEnter a healthcare review: ").strip()

    if not review:
        print("No review entered.")
        return

    review_vec = vectorizer.transform([review])
    prediction = model.predict(review_vec)[0]
    probabilities = model.predict_proba(review_vec)[0]

    class_probs = dict(zip(model.classes_, probabilities))

    print("\nPrediction:", prediction)
    print("Confidence scores:")
    for label, score in class_probs.items():
        print(f"{label}: {score:.4f}")

if __name__ == "__main__":
    main()
