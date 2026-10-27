import streamlit as st
from pymongo import MongoClient
import pandas as pd
import plotly.express as px

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Dashboard GMAO - Agentic AI",
    page_icon="🏥",
    layout="wide"
)

# Connexion MongoDB Atlas (Mets ta propre URI ici)
MONGO_URI = "mongodb+srv://saadanefatima23_db_user:UclliPpSvgCyyte8@cluster0.zqibef2.mongodb.net/?appName=Cluster0"
DB_NAME = "project"

@st.cache_resource
def init_connection():
    return MongoClient(MONGO_URI)

client = init_connection()
db = client[DB_NAME]

# Titre principal
st.title("🏥 Dashboard de Suivi & Observabilité - GMAO Biomédicale")
st.markdown("Suivi en temps réel des stocks de dispositifs médicaux, des exécutions de l'agent IA et des alertes de rupture.")

# --- CHARGEMENT DES DONNÉES ---
stock_data = list(db["stock"].find({}, {"_id": 0}))
exec_data = list(db["executions"].find({}, {"_id": 0}))
alert_data = list(db["alertes"].find({}, {"_id": 0}))

df_stock = pd.DataFrame(stock_data)
df_exec = pd.DataFrame(exec_data)
df_alert = pd.DataFrame(alert_data)

# --- SECTION 1 : KPIs / MÉTRIQUES CLÉS ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_articles = len(df_stock)
    st.metric(label="📦 Références gérées", value=total_articles)

with col2:
    ruptures_count = len(df_stock[df_stock['quantite'] < df_stock['seuil_min']]) if not df_stock.empty else 0
    st.metric(label="⚠️ Articles en rupture", value=ruptures_count, delta=-ruptures_count if ruptures_count > 0 else "Stable", delta_color="inverse")

with col3:
    total_requests = len(df_exec)
    st.metric(label="🤖 Exécutions Agent", value=total_requests)

with col4:
    avg_latency = int(df_exec['latence_ms'].mean()) if not df_exec.empty and 'latence_ms' in df_exec.columns else 0
    st.metric(label="⚡ Latence Moyenne", value=f"{avg_latency} ms")

st.markdown("---")

# --- SECTION 2 : VISUALISATION DU STOCK ET ALERTES ---
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📊 État des Stocks par Dispositif")
    if not df_stock.empty:
        # Graphique à barres interactif avec Plotly
        fig = px.bar(
            df_stock, 
            x='designation', 
            y=['quantite', 'seuil_min'], 
            barmode='group',
            labels={'value': 'Quantité', 'variable': 'Métrique', 'designation': 'Dispositif'},
            title="Comparaison Quantité Actuelle vs Seuil Minimum"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée de stock disponible.")

with col_right:
    st.subheader("🚨 Journal des Alertes Actives")
    if not df_alert.empty:
        for index, row in df_alert.tail(5).iterrows():
            st.error(f"**{row.get('type')}**\n- Réf : {row.get('reference', 'N/A')}\n- Détail : {row.get('detail', 'N/A')}")
    else:
        st.success("Aucune alerte critique en cours.")

# --- SECTION 3 : TABLEAU DÉTAILLÉ DU STOCK ---
st.subheader("📋 Inventaire Détaillé")
if not df_stock.empty:
    st.dataframe(df_stock, use_container_width=True)

# --- SECTION 4 : OBSERVABILITÉ DES EXÉCUTIONS ---
st.subheader("📈 Historique des Exécutions de l'Agent")
if not df_exec.empty:
    st.dataframe(df_exec[['correlation_id', 'date_heure', 'utilisateur', 'statut', 'latence_ms', 'cout']], use_container_width=True)
else:
    st.info("Aucun historique d'exécution pour le moment.")