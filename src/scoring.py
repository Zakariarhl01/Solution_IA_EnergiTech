import numpy as np

def calculer_seuils_dynamiques(liste_all_rul):
    """Calcule les seuils de risque basés sur la réalité statistique du parc."""
    if not liste_all_rul or len(liste_all_rul) < 5:
        return 5, 15, 30
    
    # On définit les seuils par rapport aux turbines les plus "usées"
    return (np.percentile(liste_all_rul, 10), 
            np.percentile(liste_all_rul, 25), 
            np.percentile(liste_all_rul, 50))

def calculer_score_risque(classification_panne, rul_jours, seuils):
    """
    Logique Métier : Corrélation entre détection d'anomalie et urgence temporelle.
    """
    s_critique, s_eleve, s_modere = seuils

    # NIVEAU CRITIQUE : Double validation (IA + Temps)
    if classification_panne == 1 and rul_jours <= s_critique:
        return "CRITIQUE"
    
    # NIVEAU ÉLEVÉ : Alerte préventive (soit une anomalie, soit un RUL très bas)
    elif classification_panne == 1 or rul_jours <= s_eleve:
        return "ÉLEVÉ"
    
    # NIVEAU MODÉRÉ : Maintenance à planifier
    elif rul_jours <= s_modere:
        return "MODÉRÉ"
    
    return "FAIBLE"