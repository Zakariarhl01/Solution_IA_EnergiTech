def calculer_score_risque(classification_panne, rul_jours):
    """Définit la priorité d'intervention selon les prédictions IA."""
    if classification_panne == 1 and rul_jours <= 5:
        return "CRITIQUE"
    elif classification_panne == 1 or (5 < rul_jours <= 15):
        return "ÉLEVÉ"
    elif 15 < rul_jours <= 35:
        return "MODÉRÉ"
    else:
        return "FAIBLE"
