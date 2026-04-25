from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent  

MODELS_DIR = ROOT_DIR / "models"

ASPECT_MODEL_PATH = MODELS_DIR / "best_aspect_model"
SENTIMENT_MODEL_PATH = MODELS_DIR / "sentiment_epoch18_best"