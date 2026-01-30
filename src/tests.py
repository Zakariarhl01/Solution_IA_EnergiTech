import pytest
import pandas as pd
from scoring import calculer_score_risque
from detection_anomalie import filtrer_anomalies_iqr
from langsmith import traceable

@traceable
def test_calculer_score_risque_metier():
    """Vérifie la corrélation des deux modèles."""
    seuils = (5, 15, 30)
    # CRITIQUE si panne détectée (1) ET RUL très bas (2 < 5)
    assert calculer_score_risque(1, 2, seuils) == "CRITIQUE"
    # ÉLEVÉ si panne détectée mais RUL encore correct (20 > 15)
    assert calculer_score_risque(1, 20, seuils) == "ÉLEVÉ"

@traceable
def test_filtrer_anomalies_iqr():
    """Vérifie le bon fonctionnement du filtre statistique."""
    data = {
        "turbine_id": [1, 2, 3, 4, 5, 6],
        "wind_speed": [10, 11, 10, 12, 11, 200], # 200 est l'anomalie
        "vibration_level": [5, 5, 5, 5, 5, 5],
        "temperature": [30, 31, 30, 32, 31, 30]
    }
    df = pd.DataFrame(data)
    anomalies = filtrer_anomalies_iqr(df)
    assert 200 in anomalies["wind_speed"].values