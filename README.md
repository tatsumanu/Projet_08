# Projet_08 du parcours Openclassrooms

Le but de ce projet était la conception d'un site web utilisant les données de l'API d'OpenFoodFacts pour proposer à l'utilisateur un substitut plus sain à l'aliment qui lui faisait envie.

## Fonctionnalités

Dans la version actuelle du site, l'utilisateur peut:
    . Parcourir le site
    . Effectuer des recherches d'aliments
    . Créer un compte
    . Se connecter une fois le compte créé
    . Enregistrer des aliments plus sains parmi ceux proposés par l'application
    . Consulter les aliments précédemment sauvegardés / supprimer un ou plusieurs de ces aliments

Le projet comporte deux applications principales:
    . 'Auth' qui gère la création et la gestion des utilisateurs
    . 'Nutella' est chargée de la gestion des produits alimentaires

## Prérequis

Le site fonctionne avec la version 3.0.5 de Django. Se référer au fichier requirements.txt pour l'ensemble des prérequis.
Dans cette version, le site est conçu pour être déployé sur Heroku. Il est nécessaire d'être enregistré sur cette plateforme pour effectuer le déploiement.
Le site fonctionne avec une base de donnée postgreSQL. Heroku met à disposition une base postgreSQL lors du déploiement.

## Installation et lancement du site

Se connecter à Heroku.
```bash
heroku login
```

Récupérer le projet sur votre machine.
```bash
heroku git:clone -a nom_application
cd nom_application
```

Sauvegarder le dossier en local en l'enregistrant dans git, avant d'envoyer le code vers Heroku.
```bash
git add .
git commit -am "description du commit"
git push heroku master
```

Effectuer les migrations dans le bon ordre.
```bash
heroku run python manage.py makemigrations Auth
heroku run python manage.py makemigrations Nutella
heroku run python manage.py migrate
```

Créer un administrateur pour gérer le site: plusieurs informations (email, pseudo et mot de passe) devront être données pour enregistrer cet administrateur.
```bash
heroku run python manage.py createsuperuser
```

Récupérer les aliments depuis l'API d'Openfoodfacts et les enregistrer dans la base de données.
```bash
heroku run python manage.py populate
```

A ce stade, le site déployé sur Heroku devrait être fonctionnel et accesible à l'URL 'nom_application.herokuapps.com'

## Tests

Il est possible de lancer les tests de l'application via la commande:
```bash
heroku run python manage.py test nom_application
```

Une couverture de ces tests peut même être effectuée via coverage. La deuxième commande fera apparaitre un rapport de cette couverture de tests.
```bash
heroku run python coverage run manage.py test nom_application
heroku run python coverage report
```
