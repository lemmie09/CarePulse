import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from datasets import Dataset
from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    TrainingArguments,
    Trainer
)
import numpy as np
import evaluate

IN_PATH = Path("data/processed/healthcare_reviews_min20_labeled.csv")
MODEL_DIR = Path("models/distilbert_sentiment")

def main():
    print("Loading data...")
    df = pd.read_csv(IN_PATH)

    # Keep binary classes only
    df = df[df["sentiment"] != "neutral"].copy()

    # Map labels
    label_map = {"negative": 0, "positive": 1}
    df["label"] = df["sentiment"].map(label_map)

    # Keep only required columns
    df = df[["text_clean", "label"]].dropna()
    df = df[df["text_clean"].str.strip() != ""]

    # Optional: use subset for faster training tonight
    max_samples = 20000
    if len(df) > max_samples:
        print(f"Using a subset of {max_samples} rows for faster training...")
        df = df.sample(n=max_samples, random_state=42)

    print("Train/test split...")
    train_df, test_df = train_test_split(
        df,
        test_size=0.2,
        random_state=42,
        stratify=df["label"]
    )

    train_ds = Dataset.from_pandas(train_df.reset_index(drop=True))
    test_ds = Dataset.from_pandas(test_df.reset_index(drop=True))

    print("Loading tokenizer...")
    tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

    def tokenize(batch):
        return tokenizer(
            batch["text_clean"],
            padding="max_length",
            truncation=True,
            max_length=128
        )

    print("Tokenizing...")
    train_ds = train_ds.map(tokenize, batched=True)
    test_ds = test_ds.map(tokenize, batched=True)

    train_ds = train_ds.remove_columns(["text_clean"])
    test_ds = test_ds.remove_columns(["text_clean"])
    train_ds.set_format("torch")
    test_ds.set_format("torch")

    print("Loading model...")
    model = DistilBertForSequenceClassification.from_pretrained(
        "distilbert-base-uncased",
        num_labels=2
    )

    accuracy_metric = evaluate.load("accuracy")
    f1_metric = evaluate.load("f1")

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        preds = np.argmax(logits, axis=-1)
        acc = accuracy_metric.compute(predictions=preds, references=labels)
        f1 = f1_metric.compute(predictions=preds, references=labels)
        return {
            "accuracy": acc["accuracy"],
            "f1": f1["f1"]
        }

    training_args = TrainingArguments(
        output_dir=str(MODEL_DIR / "checkpoints"),
        eval_strategy="epoch",
        save_strategy="epoch",
        logging_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=2,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        save_total_limit=1,
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=test_ds,
        compute_metrics=compute_metrics
    )

    print("Training DistilBERT...")
    trainer.train()

    print("Evaluating...")
    metrics = trainer.evaluate()
    print("\nFinal Evaluation Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    print("Saving model and tokenizer...")
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    trainer.save_model(str(MODEL_DIR))
    tokenizer.save_pretrained(str(MODEL_DIR))

    print(f"\nSaved DistilBERT model to: {MODEL_DIR}")

if __name__ == "__main__":
    main()
