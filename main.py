#importar modelos (solo se puede des de .py)
import joblib
import os

MODEL_PATH = 'ensemble_model.pkl'

# Cargar el modelo entrenado
if os.path.exists(MODEL_PATH):
    ensemble_pipeline = joblib.load(MODEL_PATH)
else:
    raise FileNotFoundError(f"No se encontró el archivo del modelo en: {MODEL_PATH}")