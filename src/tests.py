import pytest
import pandas as pd
from scoring import calculer_score_risque
from detection_anomalie import filtrer_anomalies_iqr


def test_calculer_score_risque_critique():
    # Panne prédite (1) et RUL très court (2j)
    assert calculer_score_risque(1, 2) == "CRITIQUE"


def test_calculer_score_risque_eleve():
    # Pas encore de panne directe mais RUL court (10j)
    assert calculer_score_risque(0, 10) == "ÉLEVÉ"


def test_filtrer_anomalies_iqr():
    """Vérifie que l'algorithme IQR détecte bien les valeurs hors normes."""
    data = {
        "turbine_id": [1, 2, 3, 4, 5, 6],
        "wind_speed": [10, 11, 10, 12, 11, 100],  # 100 est clairement un outlier ici
        "vibration_level": [5, 5, 5, 5, 5, 5],
        "temperature": [30, 31, 30, 32, 31, 30],
    }
    df = pd.DataFrame(data)
    anomalies = filtrer_anomalies_iqr(df)

    # Vérification : la valeur 100 doit être capturée dans le DataFrame des anomalies
    assert 100 in anomalies["wind_speed"].values
