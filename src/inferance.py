import joblib
import os
import pandas as pd
import warnings
from sklearn.exceptions import InconsistentVersionWarning

# Ignorer les messages de version
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

def charger_les_modeles():
    chemin_classif = "models/model_classification.pkl"
    chemin_regres = "models/model_regression.pkl"
    
    if os.path.exists(chemin_classif) and os.path.exists(chemin_regres):
        model_c = joblib.load(chemin_classif)
        model_r = joblib.load(chemin_regres)
        return model_c, model_r
    else:
        print("--- MODE SIMULATION ACTIVÉ ---")
        return None, None

def predire_eolienne(model_c, model_r, donnees_capteurs):
    if model_c is None or model_r is None:
        import random
        return random.choice([0, 1]), random.uniform(1, 50)
    
    # Utilisation d'un DataFrame pour éviter les carrés blancs/warnings
    colonnes = ['wind_speed', 'vibration_level', 'temperature', 'power_output', 'maintenance_done']
    df_predict = pd.DataFrame([donnees_capteurs], columns=colonnes)
    
    p_class = model_c.predict(df_predict)[0]
    p_reg = model_r.predict(df_predict)[0]
    return p_class, p_reg