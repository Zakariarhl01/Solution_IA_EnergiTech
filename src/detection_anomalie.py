import pandas as pd

def filtrer_anomalies_iqr(df):
    """
    Détecte les anomalies sur l'ensemble des données.
    """
    # On garde TOUTES les données (plus de filtre maintenance_done ici)
    df_travail = df.copy()
    
    numeric_cols = ['vibration_level', 'temperature', 'wind_speed', 'power_output']
    indices_anomalies = set()
    
    for col in numeric_cols:
        Q1, Q3 = df_travail[col].quantile(0.25), df_travail[col].quantile(0.75)
        IQR = Q3 - Q1
        lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
        
        # Repérage des outliers
        outliers = df_travail[(df_travail[col] < lower) | (df_travail[col] > upper)].index
        indices_anomalies.update(outliers)
        
    return df_travail.loc[list(indices_anomalies)]