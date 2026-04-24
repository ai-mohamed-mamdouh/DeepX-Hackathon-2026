from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import json

model_path = '/kaggle/working/aspect_model_inference'

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

with open(f"{model_path}/thresholds.json") as f:
    thresholds = json.load(f)

model.eval()

def predict_aspects(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.sigmoid(outputs.logits)[0].cpu().numpy()

    aspects = []

    for i, aspect in enumerate(aspect_cols):
        if aspect == "none":
            continue

        if probs[i] >= thresholds[aspect]:
            aspects.append(aspect)

    if len(aspects) == 0:
        aspects = ["none"]

    return aspects
