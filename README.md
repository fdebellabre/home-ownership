A simple [streamlit][https://streamlit.io/] app to compare financial outcomes over time of home ownership versus rental.

Une application [streamlit][https://streamlit.io/] pour calculer les mensualités d'un emprunt immobilier et savoir s'il vaut mieux acheter ou louer un bien immobilier (en fonction de la durée d'occupation).

Les deux scénarios confrontés sont les suivants :

1. Achat du bien, puis revente à la fin de la durée d'occupation
2. Location du bien et investissement de l'épargne constituée (l'équivalent de l'apport et des mensualités)

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
$ streamlit run main.py
```



