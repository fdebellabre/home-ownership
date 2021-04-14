A simple `streamlit` app to compare financial outcomes over time of home ownership versus rental.

Une application `streamlit` pour calculer les mensualités d'un emprunt immobilier et savoir s'il vaut mieux acheter ou louer un bien immobilier (en fonction de la durée d'occupation). L'application est [accessible ici](https://share.streamlit.io/fdebellabre/home-ownership/app.py).

Les deux scénarios confrontés sont les suivants :

1. Achat du bien, puis revente
2. Location du bien

Dans les deux cas, on suppose que l'argent ne dort jamais : l'épargne constituée est immédiatement placée.

L'application calcule le temps d'occupation minimal à partir duquel l'achat est financièrement plus intéressant que la location.



# Installation

Il n'y a pas d'installation à proprement parler, sinon des dépendances.

```bash
$ git clone https://github.com/fdebellabre/home-ownership && cd home-ownership
```

Création d'un environnement virtuel (facultatif), par exemple :

```bash
$ virtualenv venv
$ . venv/bin/activate
```

Installation des dépendances :

```bash
$ python3 -m pip install -r requirements.txt
```

# Utilisation

```bash
$ streamlit run app.py
```
