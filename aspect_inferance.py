import os
import json
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from paths import ASPECT_MODEL_PATH


tokenizer = AutoTokenizer.from_pretrained(ASPECT_MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(ASPECT_MODEL_PATH)

with open(f"{ASPECT_MODEL_PATH}/thresholds.json") as f:
    thresholds = json.load(f)

def predict_aspects(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )
    aspect_cols = [
    "food",
    "service",
    "price",
    "cleanliness",
    "delivery",
    "ambiance",
    "app_experience",
    "general",
    "none"]


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