import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from computations import *

#################### SIDEBAR

st.sidebar.markdown('# Calcul des mensualités')
prix = st.sidebar.number_input('Prix du bien immobilier', value=250000, step=1000)
apport = st.sidebar.number_input('Apport à l\'achat', value=60000, step=1000)
duree = st.sidebar.number_input('Durée de l\'emprunt (années)', 1, 50, 15, 1)
taux = st.sidebar.number_input('Taux d\'intérêt (TAEG, en %)', 0.5, 20.0, 2.0, .01)/100
notaire = st.sidebar.number_input('Frais de notaire (%)', 0.0, 20.0, 8.0, .01)/100
agence = st.sidebar.number_input('Frais d\'agence (%)', 0.0, 20.0, 5.0, .01)/100
st.sidebar.markdown('---')
st.sidebar.markdown('# Profitabilité par rapport à la location')
foncier = st.sidebar.number_input('Charges annuelles de propriété (e.g. taxe foncière)', 0, 20000, 2200, 100)
loyer = st.sidebar.number_input('Loyer pour un bien équivalent', 200, 10000, 1200, 10)
taux_alt = st.sidebar.number_input('Taux d\'intérêt du placement alternatif (%)', 0.0, 4.0, 1.0, .01)/100
taux_apprec = st.sidebar.number_input('Taux annuel d\'appréciation du bien (%)', 0.0, 4.0, 0.5, .01)/100


#################### COMPUTATIONS

vs, mens, charge, months_profitable = ownership_cost(loyer, prix, apport, duree, taux, taux_alt, notaire, agence, foncier, taux_apprec)

liste_duree = list(range(5,26))
liste_mens = []
for j in liste_duree:
    liste_mens.append(monthly_payments((prix*(1+notaire)*(1+agence)-apport), j, taux)[2][1])
df_duree = pd.DataFrame(data={"Durée de l'emprunt (années)":liste_duree, 'Mensualités':liste_mens})

liste_loyer = [z*50 for z in list(range(14,61))]
liste_profit = []
for k in liste_loyer:
    liste_profit.append(ownership_cost(k, prix, apport, duree, taux, taux_alt, notaire, agence, foncier, taux_apprec)[3])
df_loyer = pd.DataFrame(data={"Loyer équivalent":liste_loyer, "Seuil de profitabilité (mois)":liste_profit})


#################### DISPLAY

st.markdown('<center style="font-size: 50px";>Mensualités : {:,}&nbsp;€</center>'.format(round(mens)), unsafe_allow_html=True)
if np.isinf(months_profitable):
    st.markdown('<center style="font-size: 32px";>L\'achat n\'est pas profitable.</center>', unsafe_allow_html=True)
else:
    st.markdown('<center style="font-size: 32px";>Seuil de profitabilité : {:,}&nbsp;mois</center>'.format(months_profitable), unsafe_allow_html=True)

st.markdown("""
---
# Calcul des mensualités
Dans le cadre d'un emprunt aux mensualités constantes, les mensualités s'élèvent à {:,}&nbsp;€. La charge de l'emprunt, qui rémunère le prêteur, s'élève à {:,}&nbsp;€.
""".format(round(mens), round(charge)))

st.markdown("""
# Plutôt achat ou location ?
Considérons les deux scénarios suivants&nbsp;:
- Acheter le bien immobilier, y vivre, puis le revendre (sachant qu'il s'apprécie de {}&nbsp;% par an)
- Louer le bien pour {:,}&nbsp;€

Dans tous les cas, on suppose que l'argent ne dort jamais&nbsp;: l'épargne constituée est immédiatement placée au taux de {}&nbsp;%.
""".format(round(taux_apprec*100,2), loyer, round(taux_alt*100,2)))

if np.isinf(months_profitable):
    st.markdown('Résultat : l\'achat ne devient pas profitable avant 100 années d\'occupation.'.format(x=months_profitable, y=round(months_profitable/12,1)))
else:
    st.markdown('Résultat : l\'achat devient profitable à partir de **{x} mois** d\'occupation, soit {y} années.'.format(x=months_profitable, y=round(months_profitable/12,1)))

st.markdown('---')

scat_duree = px.scatter(df_duree, x="Durée de l'emprunt (années)", y="Mensualités", title='Mensualités en fonction de la durée de l\'emprunt', size=np.repeat(1, df_duree.shape[0]), size_max=7)
scat_duree.update_layout(margin=dict(l=0,r=0,b=0,t=50))
st.plotly_chart(scat_duree, config={'displayModeBar': False})

scat_loyer = px.scatter(df_loyer, x="Loyer équivalent", y="Seuil de profitabilité (mois)", title='Seuil de profitabilité en fonction du loyer équivalent', size=np.repeat(1, df_loyer.shape[0]), size_max=7)
scat_loyer.update_layout(margin=dict(l=0,r=0,b=0,t=50))
st.plotly_chart(scat_loyer, config={'displayModeBar': False})


with st.beta_expander("License et code source"):
    st.markdown("Le code est distribué sous license `GNU-GPLv3` et [accessible ici](https://github.com/fdebellabre/home-ownership).")
