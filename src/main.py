import pandas as pd
import os
import json
from inferance import charger_les_modeles, predire_eolienne
from scoring import calculer_score_risque

def executer_cockpit():
    print("--- ⚙️ Analyse du parc EnergiTech ---")
    chemin_data = "../data/energiTech_par_turbine.csv"
    
    if not os.path.exists("../tests"): os.makedirs("../tests")
    
    model_c, model_r = charger_les_modeles()
    df_entree = pd.read_csv(chemin_data)
    resultats = []

    for _, ligne in df_entree.iterrows():
        donnees = [ligne['wind_speed'], ligne['vibration_level'], 
                   ligne['temperature'], ligne['power_output'], 
                   ligne['maintenance_done']]
        
        p_class, p_rul = predire_eolienne(model_c, model_r, donnees)
        risque = calculer_score_risque(p_class, p_rul)
        
        resultats.append({
            "Turbine": int(ligne['turbine_id']),
            "Date": str(ligne['date_measure']),
            "Risque": str(risque).strip(),
            "RUL": round(float(p_rul), 1),
            "Vibration": round(float(ligne['vibration_level']), 2),
            "Temp": round(float(ligne['temperature']), 1)
        })

    with open("../tests/resultats.json", "w") as f:
        json.dump(resultats, f, indent=4)
    print(f"✅ {len(resultats)} mesures traitées et sauvegardées.")

if __name__ == "__main__":
    executer_cockpit()