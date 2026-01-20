import pandas as pd
import os
import json
from inferance import charger_les_modeles, predire_eolienne
from scoring import calculer_score_risque

def filtrer_anomalies_iqr(df):
    numeric_cols = ['vibration_level', 'temperature', 'wind_speed', 'power_output']
    indices = set()
    for col in numeric_cols:
        Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
        indices.update(df[(df[col] < lower) | (df[col] > upper)].index)
    return df.loc[list(indices)]

def traiter_donnees():
    DATA_PATH = "../data/energiTech_par_turbine.csv"
    RESULTS_PATH = "../tests/resultats.json"
    
    df_brut = pd.read_csv(DATA_PATH)
    df_anomalies = filtrer_anomalies_iqr(df_brut)
    
    model_c, model_r = charger_les_modeles()
    resultats = []

    for _, ligne in df_anomalies.iterrows():
        donnees = [ligne['wind_speed'], ligne['vibration_level'], ligne['temperature'], ligne['power_output'], ligne['maintenance_done']]
        p_class, p_rul = predire_eolienne(model_c, model_r, donnees)
        risque = calculer_score_risque(p_class, p_rul)
        
        resultats.append({
            "turbine_id": int(ligne['turbine_id']),
            "Risque": risque,
            "RUL": round(float(p_rul), 1),
            "maintenance_done": int(ligne['maintenance_done']),
            "Vibration": round(float(ligne['vibration_level']), 2),
            "Temp": round(float(ligne['temperature']), 1)
        })

    os.makedirs("../tests", exist_ok=True)
    with open(RESULTS_PATH, "w") as f:
        json.dump(resultats, f, indent=4)

if __name__ == "__main__":
    traiter_donnees()