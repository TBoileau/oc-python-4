![Centre d'échecs](logo.png)

# Centre d'échecs

## Installation
Dans un premier temps, cloner le repository :
```
git clone https://github.com/TBoileau/oc-python-4.git
```

Préparer votre environnement :
```
make prepare
```

Activer votre environnement :
```
source venv/bin/activate
```

Installer les dépendances :
```
make install
```

## Usage
Lancer l'application :
```
make run
```

Vous retrouverez les images et les fichiers CSV dans le dossier `dist/[Date et heure]/`.

## Tests
Lancer la suite de tests :
```
make tests
```

*Note : Pour le bon fonctionnement des tests, le serveur HTTP est bouchonné (mock). Vous trouverez dans le dossier `fixtures` les fichiers servies par le serveur HTTP créé spécialement pour les tests.*

## Contribuer
Veuillez prendre un moment pour lire le [guide sur la contribution](CONTRIBUTING.md).

## Changelog
[CHANGELOG.md](CHANGELOG.md) liste tous les changements effectués lors de chaque release.

## À propos
Book To Scrape a été conçu initialement par [Thomas Boileau](https://github.com/TBoileau). 
Ceci est un projet du parcours **Développeur d'application - Python** de la plateforme [Openclassrooms](https://openclassrooms.com/).
Ce projet n'a donc pas vocation a être utilisé.
Si vous avez le moindre question, contactez [Thomas Boileau](mailto:t-boileau@email.com?subject=[Github]%20Centre%20d%20echecs)
