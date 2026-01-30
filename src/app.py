import streamlit as st
import pandas as pd
import os
import json
import plotly.express as px
from langsmith import traceable

st.set_page_config(page_title="EnergiTech Cockpit", layout="wide", page_icon="⚡")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_RESULTS = os.path.join(BASE_DIR, "..", "tests", "resultats.json")

@traceable
def load_data():
    if os.path.exists(PATH_RESULTS):
        try:
            df = pd.read_json(PATH_RESULTS)
            if not df.empty:
                # Ordre logique métier pour le tri et le graphique
                ordre_risque = ["FAIBLE", "MODÉRÉ", "ÉLEVÉ", "CRITIQUE"]
                df['Risque'] = df['Risque'].astype(str).str.upper()
                df['Risque'] = pd.Categorical(df['Risque'], categories=ordre_risque, ordered=True)
            return df
        except:
            return pd.DataFrame()
    return pd.DataFrame()


@traceable
def save_data(df):
    # On repasse en format JSON standard pour la sauvegarde
    df.to_json(PATH_RESULTS, orient="records", indent=4)

st.title("⚡ EnergiTech - Cockpit Opérationnel")

df = load_data()

if not df.empty:
    # On trie pour avoir les plus critiques en haut du tableau
    df = df.sort_values("Risque", ascending=False)
    
    # KPI basés sur les éoliennes non maintenues
    a_traiter = df[df['maintenance_done'] == 0]
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🚨 CRITIQUE", len(a_traiter[a_traiter['Risque'] == "CRITIQUE"]))
    m2.metric("🟠 ÉLEVÉ", len(a_traiter[a_traiter['Risque'] == "ÉLEVÉ"]))
    m3.metric("🟡 MODÉRÉ", len(a_traiter[a_traiter['Risque'] == "MODÉRÉ"]))
    m4.metric("📊 À TRAITER", len(a_traiter))

    # Graphique Pie (Donut)
    st.write("### 📊 Répartition des urgences actives")
    fig = px.pie(a_traiter, names='Risque', color='Risque', hole=0.4,
                 color_discrete_map={
                     'CRITIQUE': '#FF4B4B', 
                     'ÉLEVÉ': '#FFA500', 
                     'MODÉRÉ': '#FFFF00', 
                     'FAIBLE': '#00CC96'
                 })
    st.plotly_chart(fig, use_container_width=True)

    # Tableau avec style conditionnel (Grisé transparent si maintenance_done == 1)
    st.write("### 🛠️ Registre complet du parc")
    
    df_vue = df.copy()
    df_vue["Valider"] = df_vue["maintenance_done"] == 1

    def style_lignes(row):
        if row['maintenance_done'] == 1:
            return ['background-color: rgba(200, 200, 200, 0.2); color: rgba(100, 100, 100, 0.5); text-decoration: line-through;'] * len(row)
        
        r = row['Risque']
        if r == "CRITIQUE":
            return ['background-color: rgba(255, 75, 75, 0.3); font-weight: bold'] * len(row)
        elif r == "ÉLEVÉ":
            return ['background-color: rgba(255, 165, 0, 0.2)'] * len(row)
        elif r == "MODÉRÉ":
            return ['background-color: rgba(255, 255, 0, 0.3)'] * len(row)
        return [''] * len(row)

    edited_df = st.data_editor(
        df_vue.style.apply(style_lignes, axis=1),
        column_config={
            "Valider": st.column_config.CheckboxColumn("Fait"),
            "turbine_id": "ID",
            "RUL": st.column_config.NumberColumn("RUL (j)", format="%d"),
            "maintenance_done": None 
        },
        disabled=[c for c in df_vue.columns if c != "Valider"],
        hide_index=True,
        use_container_width=True
    )

    if st.button("💾 Enregistrer les interventions"):
        df["maintenance_done"] = edited_df["Valider"].apply(lambda x: 1 if x else 0)
        save_data(df)
        st.success("Données synchronisées avec succès !")
        st.rerun()
else:
    st.warning("Aucune donnée disponible.")