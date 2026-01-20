import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_absolute_error

# Configuration des chemins
DATA_PATH = "../data/energiTech_par_turbine.csv"
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

def preprocess_data(df):
    """Nettoyage des données via la méthode IQR apprise en cours."""
    features = ['wind_speed', 'vibration_level', 'temperature', 'power_output']
    
    # On retire les valeurs aberrantes pour ne pas fausser l'entraînement
    for col in features:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    return df

def train():
    print("--- 🚀 Lancement du Pipeline d'Entraînement MLOps ---")
    
    # 1. Chargement des données
    if not os.path.exists(DATA_PATH):
        print("❌ Erreur : Fichier CSV introuvable.")
        return
    
    df = pd.read_csv(DATA_PATH)
    df = preprocess_data(df)
    
    # Sélection des caractéristiques (Features)
    X = df[['wind_speed', 'vibration_level', 'temperature', 'power_output', 'maintenance_done']]
    
    # --- PARTIE 1 : MODÈLE DE CLASSIFICATION (Risque de Panne) ---
    # On simule une cible 'target_panne' (1 si vibrations > 70 ou temp > 90)
    y_class = ((df['vibration_level'] > 70) | (df['temperature'] > 90)).astype(int)
    
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X, y_class, test_size=0.2, random_state=42)
    
    model_c = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model_c.fit(X_train_c, y_train_c)
    
    acc = accuracy_score(y_test_c, model_c.predict(X_test_c))
    print(f"✅ Modèle Classification entraîné (Précision : {acc:.2%})")
    joblib.dump(model_c, os.path.join(MODEL_DIR, "model_classification.pkl"))

    # --- PARTIE 2 : MODÈLE DE RÉGRESSION (RUL - Durée de vie restante) ---
    # On simule un RUL décroissant selon la chaleur et les vibrations
    y_reg = 100 - (df['temperature'] * 0.5 + df['vibration_level'] * 0.3)
    y_reg = y_reg.clip(lower=0) # Pas de jours négatifs
    
    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X, y_reg, test_size=0.2, random_state=42)
    
    model_r = RandomForestRegressor(n_estimators=100, random_state=42)
    model_r.fit(X_train_r, y_train_r)
    
    mae = mean_absolute_error(y_test_r, model_r.predict(X_test_r))
    print(f"✅ Modèle Régression entraîné (Erreur Moyenne : {mae:.2f} jours)")
    joblib.dump(model_r, os.path.join(MODEL_DIR, "model_regression.pkl"))

    print(f"--- 💾 Modèles sauvegardés dans le dossier /{MODEL_DIR} ---")

if __name__ == "__main__":
    train()