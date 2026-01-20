# ⚡ EnergiTech : Système de Maintenance Prédictive par IA

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![MLOps](https://img.shields.io/badge/Workflow-MLOps-green.svg)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)]()

## 📝 Description du Projet
Le projet **EnergiTech** vise à transformer la gestion de maintenance du parc éolien. En utilisant l'apprentissage automatique (Machine Learning), la solution analyse les données télémétriques (vibrations, température, puissance) pour détecter les anomalies et prédire les pannes avant qu'elles ne surviennent.

### Problématique métier
- **Maintenance Curative** : Coûteuse et entraîne des arrêts de production imprévus.
- **Solution IA** : Anticiper les défaillances pour planifier les interventions de manière optimale.

---

## ⚙️ Architecture Technique & MLOps

La solution adopte une approche **MLOps** modulaire pour garantir la robustesse et la scalabilité :



### 1. Ingestion & Nettoyage (`detection_anomalie.py`)
- **Méthode IQR (Interquartile Range)** : Filtrage statistique pour identifier les capteurs défaillants ou les valeurs aberrantes.
- **Features Engineering** : Sélection des variables clés (Vitesse vent, Vibrations, Température).

### 2. Entraînement des Modèles (`train_models.py`)
Le système utilise deux modèles de type **Random Forest** (Forêts Aléatoires) :
- **Classification** : Prédit la probabilité de panne (Binaire : 0 ou 1).
- **Régression** : Estime le **RUL** (Remaining Useful Life), soit le nombre de jours restants avant la défaillance.

### 3. Pipeline d'Inférence & Scoring (`inferance.py` & `scoring.py`)
- Conversion des sorties de l'IA en **niveaux de risque métier** (CRITIQUE, ÉLEVÉ, MODÉRÉ, FAIBLE).
- Calcul de priorité basé sur l'urgence (RUL faible) et la probabilité de panne.

### 4. Automatisation & CI/CD (`main.py` & `tests.py`)
L'orchestrateur `main.py` automatise la chaîne :
- **Tests Unitaires** : Validation de la logique de calcul avant chaque déploiement.
- **Pipeline Intégré** : Entraînement -> Test -> Inférence -> Lancement UI.

---

## 📂 Organisation du Répertoire
Solution_IA_EnergiTech/
├── src/
│   ├── main.py              # 🚀 Orchestrateur (Point d'entrée)
│   ├── train_models.py      # 🧠 Pipeline d'entraînement
│   ├── detection_anomalie.py # 🔍 Détection IQR
│   ├── tests.py             # 🧪 Tests unitaires
│   ├── app.py               # 🖥️ Interface Cockpit
│   ├── inferance.py         # 🔮 Moteur de prédiction
│   ├── scoring.py           # 📊 Logique de risque
│   └── models/              # 📂 Model Registry (Fichiers .pkl ici)
├── data/                    # 📂 Données sources (CSV)
├── tests/                   # 📂 Artefacts (resultats.json)
└── requirements.txt         # 📋 Dépendances