import subprocess
import sys
import os
from train_models import train
from detection_anomalie import traiter_donnees

def main():
    print("🚀 --- Lancement de la solution EnergiTech ---")

    # 1. Entraînement
    if not os.path.exists("models/model_classification.pkl"):
        print("📦 Modèles manquants, lancement de l'entraînement...")
        train()

    # 2. Tests (Correction pour Mac/Linux et environnements virtuels)
    print("\n🛠️ Exécution des tests unitaires...")
    # On utilise sys.executable -m pytest pour être sûr de trouver le module
    resultat_test = subprocess.run([sys.executable, "-m", "pytest", "tests.py"], capture_output=True, text=True)
    
    if resultat_test.returncode != 0:
        print("❌ Échec des tests. Voici le rapport d'erreur :")
        print(resultat_test.stdout)
        print(resultat_test.stderr)
        return
    else:
        print("✅ Tests validés.")

    # 3. Analyse
    print("\n🔮 Analyse du parc en cours...")
    traiter_donnees()

# 4. Interface
    print("\n🖥️ Lancement du Cockpit Streamlit...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

if __name__ == "__main__":
    main()