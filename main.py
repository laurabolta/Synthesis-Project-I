#import models (only possible from .py)
import joblib
import os

MODEL_PATH = 'ensemble_model.pkl'

# Upload trained model
if os.path.exists(MODEL_PATH):
    ensemble_pipeline = joblib.load(MODEL_PATH)
else:
    raise FileNotFoundError(f"File not found in: {MODEL_PATH}")