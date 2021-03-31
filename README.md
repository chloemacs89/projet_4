# Application centre d'échecs.

Cette application permet la gestion d'un tournoi d'échec de 8 joueurs sur 4 rondes. Ses fonctionnalités sont les suivantes : 
  * Création d'un nouveau tournoi, avec ajout de nouveaux joueurs ;
  * Gestion automatique des rondes selon le fonctionnement du tournoi Suisse ;
  * Affichage de rapports concernant la liste des joueurs, la liste des tournois ainsi que la liste des rondes et des matchs joués ;
  * Sauvegarde et récupération des données des joueurs à partir d'une base de données au format .json ;
  * Sauvegarde et récupération des données des tournoi, quelque soit l'état d'avancement, à partir d'une base de données au format .json. 
  
  
# Lancement de l'application.

Pour lancer l'application, il suffit d'entrer en ligne de commande "python chess_application.py".

# Navigation dans l'application.

Une fois lancée, l'application affiche le menu d'accueil et les options disponibles à l'utilisateur. L'application demande à l'utilisateur de choisir l'action à réaliser en entrant le chiffre correspondant à une action.

Les principaux menus et sous-menus sont les suivantes : 

  * Menu d'accueil : 
	* Création d'un nouveau tournoi ;
	* Affichage du menu du tournoi en cours ;
	* Affichage de la liste des tournois ;
	* Selection du tournoi en cours ;
	* Chargement d'un tournoi à partir de la base de données. 
	
  * Menu des tournois : 
	* Ajout de nouveaux joueurs manuellement ;
	* Ajout d'une nouvelle ronde ;
	* Accès au menu des rondes : permet l'affichage des différentes rondes et matchs inclus, ainsi que l'entrée des résultats d'une ronde ;
	* Marquage d'un tournoi comme étant achevé ;
	* Sauvegarde du tournoi à son état d'avancement ;
	* Affichage de la liste des joueurs par ordre alphabétique ou par ordre de classement ;
	* Sauvegarde des données concernant les joueurs inscrit au tournoi en cours ;
	* Ajout de joueurs à partir des données sauvegardées dans la base de données. 
	
La navigation est fluide et permet un déplacement facile entre les différentes menus et sous-menus.

Les actions permettant la sauvegarde et le chargement de données permettent aussi d'afficher les fichiers disponibles au format .json. 

# Création d'un rapport flake8 au format HTML.	
  
Pour éditer le rapport des erreurs identifiées par flake8, il suffit d'entrer la commande suivante : flake8 --format=html --htmldir=*directory-name*.

Un rapport d'erreur au format HTML est alors ajouté au dossier *directory-name* de votre choix, et peut être consulté avec n'importe quel navigateur internet.
