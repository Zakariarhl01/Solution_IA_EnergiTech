import pandas as pd
import os
import json
from langsmith import traceable
from inferance import charger_les_modeles, predire_eolienne
from scoring import calculer_score_risque, calculer_seuils_dynamiques

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "energiTech_par_turbine.csv")
RESULTS_PATH = os.path.join(BASE_DIR, "..", "tests", "resultats.json")

@traceable
def filtrer_anomalies_iqr(df):
    df_travail = df.copy()
    cols = [c for c in ["vibration_level", "temperature", "wind_speed"] if c in df.columns]
    indices = set()
    for col in cols:
        Q1, Q3 = df_travail[col].quantile(0.25), df_travail[col].quantile(0.75)
        IQR = Q3 - Q1
        indices.update(df_travail[(df_travail[col] < Q1 - 1.0*IQR) | (df_travail[col] > Q3 + 1.0*IQR)].index)
    return df_travail.loc[list(indices)]

@traceable
def traiter_donnees():
    df_brut = pd.read_csv(DATA_PATH, sep=None, engine='python')
    
    col_date = next((c for c in ['timestamp', 'Date', 'date', 'DateTime'] if c in df_brut.columns), None)
    if col_date:
        df_brut[col_date] = pd.to_datetime(df_brut[col_date])
    else:
        df_brut['Date_Temp'] = pd.Timestamp.now()
        col_date = 'Date_Temp'

    df_anomalies = filtrer_anomalies_iqr(df_brut)
    model_c, model_r = charger_les_modeles()
    
    temp_list = []
    for _, ligne in df_anomalies.iterrows():
        donnees = [ligne.get("wind_speed", 0), ligne.get("vibration_level", 0), 
                   ligne.get("temperature", 0), ligne.get("power_output", 0), 
                   ligne.get("maintenance_done", 0)]
        
        p_class, p_rul = predire_eolienne(model_c, model_r, donnees)
        
        temp_list.append({
            "turbine_id": int(ligne["turbine_id"]),
            "Date": ligne[col_date].strftime("%d/%m/%Y %H:%M") if col_date else "N/A",
            "p_class": p_class,
            "p_rul": p_rul,
            "maintenance_done": int(ligne.get("maintenance_done", 0)),
            "Vibration": round(float(ligne.get("vibration_level", 0)), 2),
            "Temp": round(float(ligne.get("temperature", 0)), 1)
        })

    if not temp_list: return

    # On ne fait pas de drop_duplicates pour garder TOUTES les lignes comme tu l'as demandé
    df_temp = pd.DataFrame(temp_list)
    seuils = calculer_seuils_dynamiques(df_temp["p_rul"].tolist())
    
    resultats_finaux = []
    for _, row in df_temp.iterrows():
        score = calculer_score_risque(row["p_class"], row["p_rul"], seuils)
        resultats_finaux.append({
            "turbine_id": row["turbine_id"],
            "Date": row["Date"],
            "Risque": score,
            "RUL": round(float(row["p_rul"]), 1),
            "maintenance_done": row["maintenance_done"],
            "Vibration": row["Vibration"],
            "Temp": row["Temp"]
        })

    with open(RESULTS_PATH, "w") as f:
        json.dump(resultats_finaux, f, indent=4)