import pandas as pd
import os
import json
from inferance import charger_les_modeles, predire_eolienne
from scoring import calculer_score_risque
from detection_anomalie import filtrer_anomalies_iqr

def executer_cockpit():
    print("--- ⚙️ Analyse et Tri par Priorité ---")
    DATA_PATH = "../data/energiTech_par_turbine.csv"
    RESULTS_PATH = "../tests/resultats.json"
    
    if not os.path.exists(DATA_PATH):
        print(f"❌ Erreur : {DATA_PATH} introuvable.")
        return
        
    df_brut = pd.read_csv(DATA_PATH)
    
    # 1. Sélection via IQR (Anomalies statistiques)
    df_suspect = filtrer_anomalies_iqr(df_brut)
    
    if df_suspect.empty:
        print("✅ Aucune anomalie détectée.")
        with open(RESULTS_PATH, "w") as f:
            json.dump([], f)
        return

    # 2. IA Inférence
    model_c, model_r = charger_les_modeles()
    resultats = []

    for idx, ligne in df_suspect.iterrows():
        donnees = [ligne['wind_speed'], ligne['vibration_level'], ligne['temperature'], ligne['power_output'], ligne['maintenance_done']]
        p_class, p_rul = predire_eolienne(model_c, model_r, donnees)
        risque = calculer_score_risque(p_class, p_rul)
        
        resultats.append({
            "turbine_id": int(ligne['turbine_id']),
            "Risque": risque,
            "RUL": round(float(p_rul), 1),
            "Vibration": round(float(ligne['vibration_level']), 2),
            "Temp": round(float(ligne['temperature']), 1),
            "maintenance_done": int(ligne['maintenance_done']),
            "Statut": "⚠️ Anomalie",
            "proba_panne": float(p_class) 
        })

    df_final = pd.DataFrame(resultats)

    # 3. TRI PAR DÉFAUT (Critique -> Faible)
    # On crée une colonne de tri invisible
    ordre_risque = {"CRITIQUE": 0, "ÉLEVÉ": 1, "MODÉRÉ": 2, "FAIBLE": 3}
    df_final['priorite'] = df_final['Risque'].map(ordre_risque)
    
    # On trie d'abord par maintenance (à faire en haut) puis par priorité
    df_final = df_final.sort_values(by=['maintenance_done', 'priorite'], ascending=[True, True])
    df_final = df_final.drop(columns=['priorite'])

    os.makedirs("../tests", exist_ok=True)
    df_final.to_json(RESULTS_PATH, orient="records", indent=4)
    print(f"✅ Analyse terminée : {len(df_final)} alertes triées par priorité.")

if __name__ == "__main__":
    executer_cockpit()