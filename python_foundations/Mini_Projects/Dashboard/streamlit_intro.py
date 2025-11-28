import streamlit as st
import pandas as pd
import plotly.express as px

# 1. PRÉPARATION DES DONNÉES
# Exactement comme avant
df = pd.DataFrame({
    "Fruit": ["Pommes", "Oranges", "Bananes", "Pommes", "Oranges", "Bananes"],
    "Ville": ["Paris", "Paris", "Paris", "Lyon", "Lyon", "Lyon"],
    "Ventes": [4, 1, 2, 2, 4, 5],
})

# 2. CONSTRUCTION DE L'APP
# Pas de "app = ...", pas de "layout = ...". On écrit direct !

st.title('Mon Premier Dashboard Streamlit')

st.write('''
    Voici la version Streamlit. Remarquez comme le code est plus court !
    Sélectionnez une ville pour filtrer le graphique :
''')

# 3. INTERACTIVITÉ (WIDGETS)
# En Dash, on devait créer le Dropdown puis faire un Callback.
# Ici, on crée le widget et on récupère sa valeur en UNE SEULE ligne.
ville_selectionnee = st.selectbox(
    'Quelle ville voulez-vous voir ?',
    df['Ville'].unique()
)

# 4. LOGIQUE & AFFICHAGE
# On utilise directement la variable 'ville_selectionnee'
filtered_df = df[df['Ville'] == ville_selectionnee]

# Création du graphique Plotly (identique à Dash)
fig = px.bar(filtered_df, x="Fruit", y="Ventes", color="Fruit", barmode="group")

# Affichage du graphique
st.plotly_chart(fig)