import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# Configuration
st.set_page_config(
    page_title="Analyse des délais Getaround",
    layout="wide"
)

# Affichage du titre
st.title('Analyse Getaround - Tableau de bord')

# Charge l'image et le Texte
image = Image.open('Getaround_title.png')
st.image(image, use_column_width=True)

st.markdown("""

Ici nous examinons l'impact des retards de retour de véhicules sur les réservations suivantes et les revenus associés. 
Les retards peuvent causer des désagréments significatifs, surtout si le véhicule est réservé pour une utilisation immédiate après le retour prévu.

Objectifs de ce tableau de bord :
- Analyser la fréquence et les conséquences des retours tardifs.
- Évaluer l'impact des retours tardifs sur les revenus des propriétaires.
- Estimer le nombre de locations affectées par l'introduction de seuils de temps entre les réservations.
- Identifier combien de complications cette mesure pourrait résoudre.

Explorons ensemble les données historiques pour comprendre les compromis entre délai minimal et impact sur l'exploitation et les revenus.

""")

# Fonctions de chargement des données
@st.cache_data
def load_data():
    fname = 'data_streamlit_price.csv'
    data = pd.read_csv(fname)
    return data

@st.cache_data
def load_data2():
    fname2 = 'data_streamlit_delay.csv'
    data2 = pd.read_csv(fname2)
    return data2

# Charge les données
data_streamlit_price = load_data()
data_streamlit_delay = load_data2()

# Calcul du coût par minute
median_price_per_day = 119  # Exemple de prix médian par jour
cost_per_minute = median_price_per_day / (24 * 60)  # Conversion du coût journalier en coût par minute

# Sidebar de la table de contenue
st.sidebar.header("Table de contenue")
st.sidebar.markdown("""
    * [Visualisation des données de délais](#prévisualisation-des-données-de-délais)
    * [Visualisation des données de prix](#prévisualisation-des-données-de-prix)
    * [Plot 1 - Nombre de locations par type de check-in et état](#plot-1---nombre-de-locations-par-type-de-check-in-et-état)
    * [Plot 2 - Répartition des retours de location à l'heure ou en retard par type de check-in](#plot-2---répartition-des-retours-de-location-à-l'heure-ou-en-retard-par-type-de-check-in)
    * [Plot 3 - Histogramme de la répartition des prix de location](#plot-3---histogramme-de-la-répartition-des-prix-de-location)
    * [Plot 4 - Analyse des puissances moteur et type de voiture par rapport aux prix de location](#plot-4---analyse-des-puissances-moteur-et-type-de-voiture-par-rapport-aux-prix-de-location)
    * [Plot 5 - Coûts estimés des retards et annulation pour différentes durées](#plot-5---coûts-estimés-des-retards-et-annulation-pour-différentes-durées)
    * [Conclusions](#conclusions)
    * [Recommandations](#recommandations)
""")
st.markdown("---")

# Visualisation des données
st.subheader('Prévisualisation des données de délais')
if st.checkbox('Visualiser les données de délais', key='show_data_delay_1'):
    st.write(data_streamlit_delay.sample(10))

st.subheader('Prévisualisation des données de prix')
if st.checkbox('Visualiser les données de prix', key='show_data_price_2'):
    st.write(data_streamlit_price.sample(10))

# Plot 1
st.subheader('Plot 1 - Nombre de locations par type de check-in et état')
fig = px.bar(data_streamlit_delay, x='checkin_type', color='state',
             title='Nombre de Locations par Type de Check-in et État',
             labels={'count': 'Nombre de Locations', 'checkin_type': 'Type de Check-in', 'state': 'État'},
             barmode='group')

fig.update_layout(xaxis_title='Type de Check-in',
                  yaxis_title='Nombre de Locations',
                  legend_title='État')

st.plotly_chart(fig, use_container_width=True)
st.markdown(
    """ Le graphe montre que les locations utilisant le check-in mobile ont un taux d'annulation plus élevé (2467) 
    par rapport au check-in connect (798), et moins de locations terminées. Cela suggère que le check-in connect, 
    avec ses avantages de flexibilité et de commodité sans contact, réduit significativement les retards et les annulations."""
    )

# Plot 2
st.subheader("Plot 2 - Répartition des retours de location à l'heure ou en retard par type de check-in")

# Sélection du type de check-in pour filtrer les données
checkin_type_option = st.selectbox('Sélectionnez le type de check-in à afficher', 
                                   ['Tous', 'mobile', 'connect'])

if checkin_type_option != 'Tous':
    filtered_data = data_streamlit_delay[data_streamlit_delay['checkin_type'] == checkin_type_option]
else:
    filtered_data = data_streamlit_delay

fig2 = px.histogram(filtered_data, x='delay_category', color='checkin_type',
                    barmode='group', histnorm='percent',
                    title="Répartition des retours de location à l'heure ou en retard par type de check-in",
                    labels={'delay': 'Catégorie de délai', 'checkin_type': 'Type de check-in'})

fig2.update_layout(xaxis_title="Catégorie de Délai",
                   yaxis_title="Pourcentage (%)",
                   legend_title="Type de Check-in")

st.plotly_chart(fig2, use_container_width=True)
st.markdown(
    """ La majorité des locations n'ont pas de retard ou ont des retards inférieurs à 10 minutes, 
    avec une prédominance des check-ins mobiles par rapport aux check-ins connect pour chaque catégorie de retard. 
    Cependant, les retards de plus de 10 minutes, y compris ceux dépassant une heure, sont également notables 
    (48 pour cent en cumulant les deux !). Ces derniers peuvent entraîner et renforcer des annulations et 
    pertes financières importantes."""
            )

# Plot 3
st.subheader('Plot 3 - Histogramme de la répartition des prix de location')
fig3 = px.histogram(data_streamlit_price, 
                    x='rental_price_per_day', 
                    nbins=50,
                    title="Histogramme de la répartition des prix de location",
                    labels={'rental_price_per_day': 'Prix de location par jour ($)'})

fig3.update_layout(
    xaxis_title="Prix de location par jour ($)",
    yaxis_title="Nombre de véhicules",
)

st.plotly_chart(fig3, use_container_width=True)
st.markdown("Prix de location médian de 119 et prix de location moyenne à 121.21 ")

# Plot 4
st.subheader('Plot 4 - Analyse des puissances moteur et type de voiture par rapport aux prix de location')

option = st.selectbox(
    "Sélectionnez le graphique à afficher pour Plot 4",
    ["Vue d'ensemble sur le type de véhicule", "Prix de location par puissance du moteur"]
)

if option == "Vue d'ensemble sur le type de véhicule":
    fig4_1 = px.scatter(data_streamlit_price, 
                        x='model_key', 
                        y='rental_price_per_day', 
                        color='engine_power',
                        title="Vue d'ensemble sur le type de véhicule et sa puissance du moteur par rapport aux prix de location")
    fig4_1.update_layout(
        xaxis_title="Modèle de véhicule",
        yaxis_title="Prix de location par jour ($)",
    )
    st.plotly_chart(fig4_1, use_container_width=True)
else:
    fig4_2 = px.scatter(data_streamlit_price,
                        x='engine_power',
                        y='rental_price_per_day',
                        color='car_type',
                        facet_col='car_type', 
                        title="Prix de location par puissance du moteur, séparé par type de voiture")
    fig4_2.update_layout(
        xaxis_title="Puissance du moteur",
        yaxis_title="Prix de location par jour ($)",
    )
    st.plotly_chart(fig4_2, use_container_width=True)

st.markdown(
    """Sans surprise, les véhicules de luxe et de sport (Ferrari, Lamborghini) ont des prix de location plus élevés, 
    corrélés à leur puissance moteur. Les SUV, convertibles et coupés sont également plus chers, 
    tandis que les hatchbacks et subcompacts restent abordables. Il aurait été très intéressant de connaitre 
    la variable du nombre de location ainsi que les taux de retards pour chaque marque/modèle 
    pour estimer précisément l'impact des pertes engendrées."""
)

# Plot 5: Coûts estimés des retards et annulation pour différentes durées
st.subheader('Plot 5 - Coûts estimés des retards et annulation pour différentes durées')
# Défini le coût par minute
cost_per_minute = 119 / 1440

# Filtre les données pour les retards terminés
mask_ended = (data_streamlit_delay['state'] == 'ended') & (data_streamlit_delay['delay_at_checkout_in_minutes'] != 'cancelled')
delayed_data = data_streamlit_delay[mask_ended].copy()

# Remplace les valeurs négatives par zéro pour le calcul des retards
delayed_data['delay_at_checkout_in_minutes'] = pd.to_numeric(delayed_data['delay_at_checkout_in_minutes'], errors='coerce')
delayed_data['delay_at_checkout_in_minutes'] = delayed_data['delay_at_checkout_in_minutes'].apply(lambda x: max(x, 0))

# Calcul du nombre de retards
count_delays = delayed_data.shape[0]

# Durées et coûts pour les retards
durations_delays = [1, 10, 30, 60]
costs_delays = [cost_per_minute * d * count_delays for d in durations_delays]

# Création du graphique pour les coûts de retards
fig_delays = go.Figure()
fig_delays.add_trace(go.Scatter(x=durations_delays, y=costs_delays, mode='lines+markers', name='Coûts dus aux retards', marker=dict(color='blue', symbol='circle')))
fig_delays.update_layout(title='Coûts estimés des retards', xaxis_title='Durée (minutes)', yaxis_title='Coût Total ($)', title_x=0.5)

# Calcul du nombre total d'annulations
tot_cancel = (data_streamlit_delay['state'] == 'canceled').sum()

# Durées et coûts pour les annulations
durations_cancellations = [60, 240, 480]
costs_cancellations = [cost_per_minute * d * tot_cancel for d in durations_cancellations]

# Création du graphique pour les coûts d'annulations
fig_cancellations = go.Figure()
fig_cancellations.add_trace(go.Scatter(x=[d / 60 for d in durations_cancellations], y=costs_cancellations, mode='lines+markers', name='Coûts dus aux annulations', marker=dict(color='red', symbol='square')))
fig_cancellations.update_layout(title='Coûts estimés des annulations', xaxis_title='Durée (heures)', yaxis_title='Coût Total ($)', title_x=0.5)

# Affichage des graphiques côte à côte dans Streamlit
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_delays, use_container_width=True)
with col2:
    st.plotly_chart(fig_cancellations, use_container_width=True)

st.markdown(""" 
    Un retard moyen d'une heure coûte environ 20 000 dollars, montant qui s'élève à plus de 45 000 dollars lorsque 
    tous les retards sont pris en compte. Par ailleurs, les annulations, souvent causées par des retards, 
    peuvent atteindre un coût total de 120 000 dollars pour une durée de 8 heures."""
            )

# Conclusions et Recommandations
st.subheader('Conclusions')

# Charge les données (pour s'assurer qu'elles n'ont pas été modifiées)
data_streamlit_delay = load_data2()

# Calcul des statistiques de base pour les retards
tot_data = data_streamlit_delay.shape[0]  # nombre total de locations
mask_0 = data_streamlit_delay.state == "canceled"
tot_cancel = mask_0.sum()  # nombre total de cas annulés
tot_cancel_percent = round(100. * (tot_cancel / tot_data), 1)  # pourcentage
tot_ended = tot_data - tot_cancel  # nombre total de cas terminés

col_ = "delay_at_checkout_in_minutes"
data_streamlit_delay[col_] = pd.to_numeric(data_streamlit_delay[col_].replace('cancelled', np.nan), errors='coerce')
data_streamlit_delay[col_] = data_streamlit_delay[col_].apply(lambda x: max(x, 0))

# Calcul des retards
mask_a = data_streamlit_delay[col_] >= 0.0
tot_delay_today = mask_a.sum()  # nombre total de retards
tot_delay_today_percent = round(100. * (tot_delay_today / tot_ended), 1)  # pourcentage

st.write("1. ", tot_delay_today, " (", tot_delay_today_percent, "pour cent) des conducteurs étaient en retard pour le prochain check-in.")
st.write("2. Cela a peut-être entraîné ", tot_cancel, " (", tot_cancel_percent, " pour cent) d'utilisateurs à annuler leurs demandes de location.")

st.markdown("""
    Les retards augmentent les chances qu'une course soit annulée, ce qui fait perdre de l'argent à l'entreprise. Cela augmente le risque financier.
    Il est fortement recommandé d'optimiser le risque financier en introduisant un seuil de retard.
""")

# Slider pour définir le seuil de retard
input_threshold = st.slider('Définir le seuil de retard (en minutes)', 0, 150, step=5)

try:  # en cas d'interaction de l'utilisateur avec le slider
    mask_b = data_streamlit_delay[col_] >= input_threshold
except BaseException:  # en cas d'absence d'interaction de l'utilisateur avec le slider
    mask_b = mask_a

tot_delay_tomorrow = mask_b.sum()  # nombre de retards après introduction du seuil
# nombre de cas de retard résolus
change_delay = tot_delay_today - tot_delay_tomorrow
change_delay_percent = round(100. * change_delay / tot_ended, 1)

st.write("\n\t :star: Si le seuil de retard ci-dessus avait été introduit, ", change_delay, " (", change_delay_percent, " pour cent) des cas problématiques auraient été résolus.\n")

# Sélection du type de check-in
type_checkin = st.selectbox('Sélectionnez la fonctionnalité du type de check-in', ["Connect uniquement"])

mask_c = data_streamlit_delay["checkin_type"] == "connect"
total_delay_connect = (mask_a & mask_c).sum()
total_delay_connect_percent = round(100. * (total_delay_connect / tot_delay_today), 1)
tot_delay_tomorrow_percent = tot_delay_today_percent - total_delay_connect_percent

if type_checkin == "Connect uniquement":
    st.write("\t Avec l'utilisation du type de check-in 'connect', ", tot_delay_tomorrow_percent, " pour cent des cas problématiques pourrait être amélioré. \n")

st.subheader('Recommandations')
st.markdown(""" 
    Nous pouvons constater que des retards pourraient être évités par la mise en place d'un système de retards préventifs. 
    Les données initiales suggèrent également que le check-in 'connect' pourrait réduire les retards. 
    Cependant, il est important de prendre en compte la différence de taille des échantillons et de considérer des 
    méthodes supplémentaires pour vérifier ces résultats. Une approche plus rigoureuse, comme des tests A/B 
    ou une analyse par cohortes, pourrait fournir des insights plus robustes.""")
