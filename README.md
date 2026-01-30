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

## Installation & Setup

1. **Clone le repository:**

   ```bash
   git clone https://github.com/Zakariarhl01/Solution_IA_EnergiTech.git
   cd Solution_IA_EnergiTech
   ```

2. **Installe les dépendances:**

   ```bash
   pip install -r requirements.txt

   ```

3. **Prépare ta clé LangSmith**

    Dans le fichier `.env` à la racine du projet, stocke

    ```
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
    LANGCHAIN_API_KEY=votre_cle_api_langsmith
    LANGCHAIN_PROJECT=votre_projet
    LANGCHAIN_WORKSPACE_ID=votre_id
    ```
    Lien pour générer une API key [LangSmith](https://smith.langchain.com/).
---

# Licence et Droits d'Utilisation

Ce projet est publié sous la Licence MIT, offrant une flexibilité maximale pour l'utilisation, la modification et la distribution.

- Autorisations : La licence MIT accorde aux utilisateurs le droit d'utilisation commerciale sans restrictions ni redevances, la modification et la création d'œuvres dérivées, la distribution de versions originales ou modifiées, l'utilisation privée à des fins internes et l'utilisation de brevets pour les implémentations. Les organisations de toute taille peuvent adopter ce projet, l'intégrer dans des produits commerciaux, le modifier pour répondre à des besoins spécifiques et le déployer dans n'importe quel contexte commercial sans contraintes légales ni frais de licence.

- Limitations : Le logiciel est fourni « en l'état », sans aucune garantie d'aucune sorte. Aucune responsabilité n'est acceptée pour les dommages ou pertes découlant de son utilisation. Aucun droit de marque n'est accordé au-delà de ceux explicitement énoncés. Ces limitations standard protègent le projet tout en maintenant une large utilisabilité.

- Conditions : Les utilisateurs doivent inclure l'avis de droit d'auteur (copyright) original dans les distributions ainsi que le texte de la licence avec les copies du logiciel. Ces exigences minimales garantissent une attribution appropriée tout en permettant une flexibilité maximale de déploiement et de modification.

Le texte complet de la licence se trouve dans le fichier LICENSE à la racine du dépôt. Cette approche permissive maximise l'impact potentiel du projet sur l'accessibilité de l'intelligence d'affaires (Business Intelligence) pour divers contextes organisationnels, des startups aux grandes entreprises.


# Auteurs

Ibrahima Sory DIALLO
Etudiant en Bachelor IA / DATA
Disponible sur linkedin https://www.linkedin.com/in/ibrahima-sory-diallo-isd/

Zakaria RAHAL
Étudiant en Bachelor IA / DATA
Disponible sur linkedin https://www.linkedin.com/in/zakaria-rahal-a88a75330/
Portfolio https://zakaria-rahal.fr/

Prince