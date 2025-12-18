def calculer_score_risque(classification_panne, rul_jours):
    """
    Traduit les prédictions IA en catégories de risque métier.
    classification_panne: 1 si panne prévue sous 7j, 0 sinon
    rul_jours: estimation du nombre de jours restants avant panne
    """
    if classification_panne == 1 and rul_jours <= 3:
        return "CRITIQUE"
    
    elif classification_panne == 1 or (3 < rul_jours <= 7):
        return "ÉLEVÉ"
    
    elif 7 < rul_jours <= 15:
        return "MODÉRÉ"
    
    else:
        return "FAIBLE"