import subprocess
import sys
import os
# from train_models import train
from src.train_models import train
# from detection_anomalie import traiter_donnees
from src.detection_anomalie import traiter_donnees

def main():
    print("🚀 --- Lancement de la solution EnergiTech ---")

    # 1. Pipeline d'Entraînement
    # On force le ré-entraînement pour appliquer les nouveaux seuils
    print("📦 Mise à jour des modèles IA...")
    train()

    # 2. Tests de Qualité (CI)
    print("\n🛠️ Exécution des tests unitaires...")
    res = subprocess.run([sys.executable, "-m", "pytest", "tests.py"], capture_output=True, text=True)
    if res.returncode != 0:
        print("❌ Échec des tests :\n", res.stdout)
        return
    print("✅ Tests validés.")

    # 3. Analyse & Scoring
    print("\n🔮 Analyse du parc en cours...")
    traiter_donnees()

    # 4. Déploiement
    print("\n🖥️ Lancement du Cockpit Streamlit...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

if __name__ == "__main__":
    main()