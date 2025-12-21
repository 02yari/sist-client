import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "model.pkl")

model = joblib.load(MODEL_PATH)

def predict_churn(data):
    """
    data = [edad, antiguedad_meses, frecuencia_uso, reclamos, pagos_atrasados]
    """
    prediction = model.predict([data])[0]
    probability = model.predict_proba([data])[0][1]

    return prediction, probability
