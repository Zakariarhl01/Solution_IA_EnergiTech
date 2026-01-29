import streamlit as st
import pandas as pd
import os
import plotly.express as px
from langsmith import traceable

st.set_page_config(page_title="EnergiTech Cockpit", layout="wide", page_icon="⚡")

PATH_RESULTS = "../tests/resultats.json"

st.html("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>")

@traceable  
def load_data():
    if os.path.exists(PATH_RESULTS):
        df = pd.read_json(PATH_RESULTS)
        if not df.empty:
            df['Risque'] = df['Risque'].astype(str).str.upper()
        return df
    return pd.DataFrame()


@traceable
def save_data(df):
    df.to_json(PATH_RESULTS, orient="records", indent=4)

st.title("⚡ EnergiTech - Cockpit Opérationnel")

df = load_data()

if not df.empty:
    # --- KPI ---
    a_traiter = df[df['maintenance_done'] == 0]
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🚨 CRITIQUE", len(a_traiter[a_traiter['Risque'] == "CRITIQUE"]))
    m2.metric("🟠 ÉLEVÉ", len(a_traiter[a_traiter['Risque'] == "ÉLEVÉ"]))
    m3.metric("🟡 MODÉRÉ", len(a_traiter[a_traiter['Risque'] == "MODÉRÉ"]))
    m4.metric("✅ RÉPARÉES", len(df[df['maintenance_done'] == 1]))

    st.markdown("---")

    col_graph, col_tab = st.columns([1, 2])

    with col_graph:
        st.subheader("📊 Répartition des Risques")
        if not a_traiter.empty:
            fig = px.pie(a_traiter, names='Risque', color='Risque',
                         color_discrete_map={'CRITIQUE': '#ff4b4b', 'ÉLEVÉ': '#ffa500', 
                                             'MODÉRÉ': '#ffff00', 'FAIBLE': '#2ecc71'},
                         hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("Aucune maintenance en attente.")

    with col_tab:
        st.subheader("📋 Registre des Interventions")
        
        # Filtre latéral
        vue = st.sidebar.radio("Filtrer la liste :", ["Toutes", "⏳ À traiter", "✅ Déjà gérées"])
        df_vue = df.copy()
        if vue == "⏳ À traiter": df_vue = df[df['maintenance_done'] == 0].copy()
        elif vue == "✅ Déjà gérées": df_vue = df[df['maintenance_done'] == 1].copy()

        # Ajout de la colonne de validation
        df_vue.insert(0, "Valider", False)

        # --- LOGIQUE DES COULEURS PAR LIGNE ---
        def style_lignes(row):
            # 1. Si déjà réparé : Gris et barré
            if row['maintenance_done'] == 1:
                return ['color: #888; text-decoration: line-through; background-color: rgba(200,200,200,0.1)'] * len(row)
            
            # 2. Couleurs selon le risque pour les tâches à faire
            r = row['Risque']
            if r == "CRITIQUE":
                return ['background-color: rgba(255, 75, 75, 0.4); color: white; font-weight: bold'] * len(row)
            elif r == "ÉLEVÉ":
                return ['background-color: rgba(255, 165, 0, 0.3)'] * len(row)
            elif r == "MODÉRÉ":
                return ['background-color: rgba(255, 255, 0, 0.2)'] * len(row)
            return [''] * len(row)

        # Affichage du tableau
        edited_df = st.data_editor(
            df_vue.style.apply(style_lignes, axis=1),
            column_config={
                "Valider": st.column_config.CheckboxColumn("Réparé"),
                "turbine_id": "ID Turbine",
                "Risque": "Priorité",
                "RUL": st.column_config.NumberColumn("RUL (J)", format="%d j"),
                "maintenance_done": None,
                "proba_panne": None
            },
            disabled=[c for c in df_vue.columns if c != "Valider"],
            hide_index=True,
            use_container_width=True,
            height=450
        )

        # Action de validation
        selection = edited_df[edited_df["Valider"] == True]
        if not selection.empty:
            if st.button(f"🚀 Valider {len(selection)} réparation(s)"):
                ids = selection['turbine_id'].tolist()
                df.loc[df['turbine_id'].isin(ids), 'maintenance_done'] = 1
                save_data(df)
                st.rerun()
else:
    st.info("Lancez 'main.py' pour générer les données.")
