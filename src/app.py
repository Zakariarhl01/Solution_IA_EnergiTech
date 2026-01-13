import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(page_title="EnergiTech Cockpit", layout="wide")

# --- CACHE DES DONNÉES ---
@st.cache_data
def load_data(path):
    if os.path.exists(path):
        df = pd.read_json(path)
        df = df.reset_index(drop=True)
        # Nettoyage pour éviter les bugs de casse ou d'espaces
        df['Risque'] = df['Risque'].astype(str).str.strip().str.upper()
        return df
    return None

st.title("⚡ EnergiTech - Cockpit Opérationnel")

path_json = "../tests/resultats.json"
df = load_data(path_json)

if df is not None:
    # --- 1. LÉGENDE DES COLONNES ---
    with st.expander("ℹ️ Guide de lecture du tableau"):
        st.markdown("""
        - **Turbine** : Identifiant de l'éolienne | **Date** : Date du relevé
        - **Risque** : Niveau de priorité calculé par l'IA
        - **RUL** : Jours restants avant panne estimée
        - **Vibration** : Intensité vibratoire (G) | **Temp** : Chaleur interne (°C)
        """)

    # --- 2. BARRE LATÉRALE (Filtres & Recherche) ---
    st.sidebar.header("🔍 Recherche & Tris")
    search = st.sidebar.text_input("Rechercher ID Turbine :", placeholder="Ex: 15")
    
    risques_dispo = ["CRITIQUE", "ÉLEVÉ", "MODÉRÉ", "FAIBLE"]
    sel_risques = st.sidebar.multiselect("Filtrer par Risque :", risques_dispo, default=risques_dispo)
    
    ordre_tri = st.sidebar.selectbox("Trier par :", ["Priorité (Urgence)", "ID Turbine", "RUL (Jours)"])

    # --- 3. TRAITEMENT DES DONNÉES (Filtrage & Tri) ---
    df_f = df[df['Risque'].isin(sel_risques)].copy()
    
    if search:
        df_f = df_f[df_f['Turbine'].astype(str).str.contains(search)]

    # Logique de tri
    ordre_risque_map = {"CRITIQUE": 0, "ÉLEVÉ": 1, "MODÉRÉ": 2, "FAIBLE": 3}
    df_f['Priorite_Num'] = df_f['Risque'].map(ordre_risque_map)
    
    if ordre_tri == "Priorité (Urgence)":
        df_f = df_f.sort_values(by=['Priorite_Num', 'RUL'])
    elif ordre_tri == "ID Turbine":
        df_f = df_f.sort_values(by='Turbine')
    else:
        df_f = df_f.sort_values(by='RUL')

    # --- 4. COMPTEURS (KPI) ---
    st.subheader("📊 État actuel du parc")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🚨 CRITIQUE", len(df_f[df_f['Risque'] == "CRITIQUE"]))
    m2.metric("🟠 ÉLEVÉ", len(df_f[df_f['Risque'] == "ÉLEVÉ"]))
    m3.metric("🟡 MODÉRÉ", len(df_f[df_f['Risque'] == "MODÉRÉ"]))
    m4.metric("🟢 FAIBLE", len(df_f[df_f['Risque'] == "FAIBLE"]))

    st.markdown("---")

    # --- 5. GRAPHIQUE & TABLEAU ---
    col_chart, col_table = st.columns([1, 2])

    with col_chart:
        fig = px.pie(df_f, names='Risque', color='Risque',
                     color_discrete_map={'CRITIQUE': '#ff4b4b', 'ÉLEVÉ': '#ffa500', 
                                         'MODÉRÉ': '#ffff00', 'FAIBLE': '#2ecc71'},
                     title="Répartition des risques filtrés")
        st.plotly_chart(fig, use_container_width=True)

    with col_table:
        st.write(f"📋 **Top 300 des interventions** (sur {len(df_f)} lignes)")
        
        def style_dynamique(row):
            r = row['Risque']
            if r == "CRITIQUE": return ['background-color: #ff4b4b; color: white'] * len(row)
            if r == "ÉLEVÉ": return ['background-color: #ffa500; color: black'] * len(row)
            if r == "MODÉRÉ": return ['background-color: #ffff00; color: black'] * len(row)
            if r == "FAIBLE": return ['background-color: #2ecc71; color: white'] * len(row)
            return [''] * len(row)

        # On cache la colonne de tri technique et on limite l'affichage pour la fluidité
        df_display = df_f.drop(columns=['Priorite_Num']).head(300)
        
   
        # 1. On ajoute une colonne pour la sélection (décochée par défaut)
    df_display.insert(0, "Sélection", False)

# 2. On configure l'éditeur pour qu'il soit interactif
    st.data_editor(
      df_display.style.apply(style_dynamique, axis=1),
        column_config={
            "Sélection": st.column_config.CheckboxColumn(
                "Fait",
                help="Marquer comme maintenu",
                default=False,
            )
        },
        disabled=["Turbine", "Risque", "RUL", "Vibration", "Temp"], # On ne peut modifier que la checkbox
        use_container_width=True,
        height=450,
        hide_index=True,    
    )
        
    if len(df_f) > 300:
        st.info("💡 L'affichage est limité aux 300 premières lignes pour rester fluide.")

else:
    st.error("Données introuvables. Lancez d'abord 'python3 main.py'.")