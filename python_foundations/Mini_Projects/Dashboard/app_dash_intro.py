import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# 1. PRÉPARATION DES DONNÉES (PANDAS)
# Créons un petit DataFrame pour l'exemple
df = pd.DataFrame({
    "Fruit": ["Pommes", "Oranges", "Bananes", "Pommes", "Oranges", "Bananes"],
    "Ville": ["Paris", "Paris", "Paris", "Lyon", "Lyon", "Lyon"],
    "Ventes": [4, 1, 2, 2, 4, 5],
})

# 2. INITIALISATION DE L'APPLICATION (DASH)
app = dash.Dash(__name__)

# 3. DÉFINITION DE LA MISE EN PAGE (LAYOUT)
# C'est ici qu'on dessine l'apparence de notre page web (HTML via Python)
app.layout = html.Div(children=[
    
    html.H1(children='Mon Premier Tableau de Bord'),

    html.Div(children='''
        Un dashboard interactif créé avec Dash et Plotly.
        Sélectionnez une ville pour filtrer le graphique :
    '''),

    # L'élément interactif (Liste déroulante)
    dcc.Dropdown(
        id='filtre-ville',
        options=[{'label': ville, 'value': ville} for ville in df['Ville'].unique()],
        value='Paris', # Valeur par défaut
        clearable=False
    ),

    # L'endroit où le graphique va s'afficher
    dcc.Graph(
        id='graphique-ventes'
    )
])

# 4. LA LOGIQUE INTERACTIVE (CALLBACKS)
# C'est la magie de Dash : connecter l'entrée (Dropdown) à la sortie (Graphique)
@app.callback(
    Output('graphique-ventes', 'figure'),
    Input('filtre-ville', 'value')
)
def update_graph(ville_selectionnee):
    # a. On filtre les données Pandas en fonction du choix de l'utilisateur
    filtered_df = df[df['Ville'] == ville_selectionnee]

    # b. On crée le graphique Plotly avec ces données filtrées
    fig = px.bar(filtered_df, x="Fruit", y="Ventes", color="Fruit", barmode="group")
    
    # c. On retourne le graphique pour qu'il s'affiche
    return fig

# 5. LANCEMENT DU SERVEUR
if __name__ == '__main__':
    print("L'application tourne ! Ouvrez ce lien dans votre navigateur : http://127.0.0.1:8050/")
    app.run(debug=True)