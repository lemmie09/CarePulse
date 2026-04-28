from pathlib import Path
import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

MODEL_DIR = Path("models/distilbert_sentiment")

def main():
    print("Loading DistilBERT model...")
    tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_DIR)
    model = DistilBertForSequenceClassification.from_pretrained(MODEL_DIR)
    model.eval()

    label_map = {0: "negative", 1: "positive"}

    while True:
        text = input("\nEnter a healthcare review (or type 'exit'): ").strip()
        if text.lower() == "exit":
            break
        if not text:
            print("Please enter some text.")
            continue

        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128
        )

        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)[0]
            pred_idx = torch.argmax(probs).item()

        print("\nPrediction:", label_map[pred_idx])
        print("Confidence scores:")
        print(f"negative: {probs[0].item():.4f}")
        print(f"positive: {probs[1].item():.4f}")

if __name__ == "__main__":
    main()
