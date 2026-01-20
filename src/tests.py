import pytest
import pandas as pd
from scoring import calculer_score_risque
from detection_anomalie import filtrer_anomalies_iqr

def test_calculer_score_risque_critique():
    """Vérifie la logique métier : Panne imminente."""
    assert calculer_score_risque(1, 2) == "CRITIQUE"

def test_calculer_score_risque_faible():
    """Vérifie la logique métier : Turbine saine."""
    assert calculer_score_risque(0, 40) == "FAIBLE"

def test_filtrer_anomalies_iqr():
    """Vérifie que l'algorithme IQR détecte bien les valeurs hors normes."""
    data = {
        'turbine_id': [1, 2, 3, 4, 5],
        'wind_speed': [15, 15, 15, 15, 500], # Outlier
        'vibration_level': [20, 20, 20, 20, 20],
        'temperature': [50, 50, 50, 50, 50],
        'power_output': [1000, 1000, 1000, 1000, 1000]
    }
    df_test = pd.DataFrame(data)
    anomalies = filtrer_anomalies_iqr(df_test)
    assert 500 in anomalies['wind_speed'].values