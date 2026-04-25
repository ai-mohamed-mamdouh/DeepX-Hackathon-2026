import json
import os
import torch
import numpy as np

from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from paths import SENTIMENT_MODEL_PATH


tokenizer = AutoTokenizer.from_pretrained(SENTIMENT_MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(SENTIMENT_MODEL_PATH)

def predict_sentiment(text, aspect):
    input_text = str(text) + " </s> aspect: " + str(aspect)

    inputs = tokenizer(
        input_text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(outputs.logits, dim=1)[0].cpu().numpy()
    pred_id = int(np.argmax(probs))

    return {
        "label": model.config.id2label[pred_id],
        "confidence": float(probs[pred_id]),
        "probs": {
            model.config.id2label[i]: float(probs[i])
            for i in range(len(probs))
        }
    }