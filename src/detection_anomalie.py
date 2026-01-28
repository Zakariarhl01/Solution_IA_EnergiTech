import pandas as pd
import os
import json
from inferance import charger_les_modeles, predire_eolienne
from scoring import calculer_score_risque


def filtrer_anomalies_iqr(df):
    """Détection élargie pour correspondre aux statistiques globales."""
    df_travail = df.copy()
    numeric_cols = ["vibration_level", "temperature", "wind_speed"]
    indices_anomalies = set()

    for col in numeric_cols:
        Q1, Q3 = df_travail[col].quantile(0.25), df_travail[col].quantile(0.75)
        IQR = Q3 - Q1
        # Coefficient 1.0 au lieu de 1.5 pour inclure plus de turbines (environ 15% du parc)
        lower, upper = Q1 - 1.0 * IQR, Q3 + 1.0 * IQR
        outliers = df_travail[
            (df_travail[col] < lower) | (df_travail[col] > upper)
        ].index
        indices_anomalies.update(outliers)

    return df_travail.loc[list(indices_anomalies)]


def traiter_donnees():
    DATA_PATH = "../data/energiTech_par_turbine.csv"
    RESULTS_PATH = "../tests/resultats.json"

    df_brut = pd.read_csv(DATA_PATH)
    df_anomalies = filtrer_anomalies_iqr(df_brut)

    model_c, model_r = charger_les_modeles()
    resultats = []

    for _, ligne in df_anomalies.iterrows():
        donnees = [
            ligne["wind_speed"],
            ligne["vibration_level"],
            ligne["temperature"],
            ligne["power_output"],
            ligne["maintenance_done"],
        ]
        p_class, p_rul = predire_eolienne(model_c, model_r, donnees)
        risque = calculer_score_risque(p_class, p_rul)

        resultats.append(
            {
                "turbine_id": int(ligne["turbine_id"]),
                "Risque": risque,
                "RUL": round(float(p_rul), 1),
                "maintenance_done": int(ligne["maintenance_done"]),
                "vibration_level": round(float(ligne["vibration_level"]), 2),
                "temperature": round(float(ligne["temperature"]), 1),
            }
        )

    os.makedirs("../tests", exist_ok=True)
    # Trie les résultats par score de risque décroissant avant de dédoublonner
    resultats.sort(key=lambda x: x["Risque"], reverse=True)

    seen_ids = set()
    resultats_uniques = []

    for res in resultats:
        if res["turbine_id"] not in seen_ids:
            resultats_uniques.append(res)
            seen_ids.add(res["turbine_id"])

    with open(RESULTS_PATH, "w") as f:
        json.dump(resultats_uniques, f, indent=4)


if __name__ == "__main__":
    traiter_donnees()
