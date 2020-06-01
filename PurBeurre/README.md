# README DU PROJET 8

## Présentation

L'objectif de ce projet est de récupérer des données mises à disposition par l'API OpenFoodFacts afin de développer une solution web fullstack avec le framework backend Django.

Le client est PurBeurre comme au projet 5.
D'après le cahier des charges qu'il nous a fourni il souhaite:
- l'utilisation de sa charte graphique
- l'intégration d'un template téléchargeable
- des couleurs chaudes 
- cette icône de carotte pour le menu. 
- une photo qu'il a choisie en fond de la page d’accueil.

Le projet est suivi sur Trello et le produit final est accessible à l’adresse 
(https://beurrepur.herokuapp.com/) 

## Lien GitHub: 
(https://github.com/nojoven/Projet8) 

## Exécution

    • L’environnement virtuel a été généré avec pipenv install.	
    • La commande pipenv install nom_de_mon_module permet d'installer des modules python.	
    • La commande pipenv graph liste les modules installés.	
    • En local il faudra donc utiliser pipenv shell  avant de pouvoir démarrer le serveur (localhost:8000).
    • Projet Django créé avec manage.py 
    • Ajout du chemin vers les variables d’environnement: $env:DJANGO_SETTINGS_MODULE='PurBeurre.settings'
    • Migration du modèle de données avec  manage.py makemigrations suivi de manage.py migrate
    • Lancement local avec python manage.py runserver
    • Remplissage local de la basse de données: manage.py fill_db
    • Déploiement sur serveur loca:   python manage.py runserver
    • Remplissage Heroku de la basse de données: 
      heroku run manage.py fill_db
      (nécessite heroku run python manage.py migrate )
	• De manière générale toutes les commandes manage.py peuvent être lancées sur Heroku. 
	  Il faut alors les faire précéder de   heroku run. Exemple: heroku runpython manage.py fill_db 		
    • Liste des requirements accessible avec pip freeze et actualisable avec pip freeze > requirements.txt
    • Le fichier pytest.ini, à la racine, permet de lancer en un appel de pytest tous les tests du projet
    • Exécution des tests d’intégration: python manage.py test
    • Tests de couverture: pytest-cov suivi de coverage report (voir documentation de la stratégie de tests)
    • Depuis la fin du projet   pytest --cov=.    lance l'ensemble des tests
    • Lecture des logs heroku: heroku logs --tail

## Résolution des problèmes
	• En cas de dysfonctionnement au niveau des migrations
		1) python manage.py migrate --fake foodfacts zero    
		2) supprimer les migrations (fichiers)
		3) python manage.py makemigrations  
		4) python manage.py migrate --fake-initial 
		5) python manage.py fill_db
		6) versionner  et pousser les modifications
		7) déployer
		8) supprimer la base de données heroku (add-on postgres)
		9) la recréer en remettant l'add-on
		10) créer un server dans PgAdmin à partir des données de configiration de l'add on
		11) heroku run python manage.py makemigrations
		12) heroku run python manage.py migrate
		13) heroku run python manage.py fill_db
		



