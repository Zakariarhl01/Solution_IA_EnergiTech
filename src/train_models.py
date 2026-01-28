import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import joblib
import os


def train():
    DATA_PATH = "../data/energiTech_par_turbine.csv"
    MODEL_DIR = "models"
    os.makedirs(MODEL_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    # --- ÉTIQUETAGE SENSIBLE (Pour éviter d'avoir uniquement du "Faible") ---
    # On considère une panne si Temp > 45°C ou Vibration > 25
    y_class = ((df["vibration_level"] > 25) | (df["temperature"] > 45)).astype(int)

    # RUL dégradé plus rapidement pour simuler l'urgence
    y_reg = 100 - (df["temperature"] * 1.2 + df["vibration_level"] * 0.8)
    y_reg = y_reg.clip(lower=0)

    X = df[
        [
            "wind_speed",
            "vibration_level",
            "temperature",
            "power_output",
            "maintenance_done",
        ]
    ]

    # Entraînement
    model_c = RandomForestClassifier(n_estimators=100, random_state=42)
    model_r = RandomForestRegressor(n_estimators=100, random_state=42)

    model_c.fit(X, y_class)
    model_r.fit(X, y_reg)

    joblib.dump(model_c, os.path.join(MODEL_DIR, "model_classification.pkl"))
    joblib.dump(model_r, os.path.join(MODEL_DIR, "model_regression.pkl"))
    print("✅ Modèles IA mis à jour et sauvegardés dans src/models/")


if __name__ == "__main__":
    train()
