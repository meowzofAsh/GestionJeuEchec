♟️ Projet de Gestion de Tournois d'Échecs (Système Suisse)

Auteur : [OPERI CARLA-MARIA]  
Date : [JEUDI 16 OCTOBRE 2025]  

Description :Ce programme console, développé en Python, implémente un système de gestion de tournois d'échecs basé sur l'architecture MVC (Modèle-Vue-Contrôleur) et utilise la base de données légère TinyDB pour la persistance des données. Il respecte le format d'appariement du "Système Suisse".


🛠️ Technologies et Prérequis

Langage: Python 
Architecture: MVC (Modèle-Vue-Contrôleur)
Persistance des données: TinyDB
Librairies clés:
     `tinydb` : Base de données NoSQL légère.
     `flake8`, `flake8-html` : Outils d'analyse de la qualité du code (linters).


🚀 Installation et Démarrage

Suivez les étapes ci-dessous pour configurer l'environnement et lancer l'application.

1. Cloner le Dépôt:

git clone [(https://github.com/meowzofAsh/GestionJeuEchec/tree/main)]
cd [GestionJeuEchec]

2. Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows (PowerShell)
.\venv\Scripts\activate
# Sur Linux/macOS
source venv/bin/activate

3. lancement du programme

python main.py
(Le programme démarrera et chargera les données existantes à partir de db.json, ou commencera avec une base vide.)

---


💡 Mode d'Emploi

Le programme fonctionne via un menu de console interactif. Le déroulement typique est le suivant :

1.  *Gérer les joueurs* (Option 1) : Enregistrer un minimum de **8 joueurs** avant de créer un tournoi.
    (option A) : Ajouter joueur (ajoue 1 joueur en l'occurence le nom, le prenom, le classement, la date de naissance, les points )
    (option M) : Modifier classement (modifie le classement en fonction des points enregistrer lors d'un tournoi )
    (option T) : Trier (afficher) (trie les joueur en fonction de leurs classement)
    (option R) : Retour (retourne au précedent)

2.  *Créer un nouveau tournois* (Option 2) : Définir les paramètres du tournoi et y ajouter les 8 joueurs enregistrés.
    (option A) : Créer un tournoi (Créer et ajouter dans la BD un tournoi avec son nom, le lieu, la date de debut et la date de fin )
    (option V) : Voir les détails d’un tournoi (Permet de voir les detail d'un tournoi grace a so ID unique, le lieu, la date(debut-fin) le controle (Blitz,rapide), le nombre de tours prevu(4 selon le directeur))
    (option R) : Retour (retourne au précedent)
3.  *Lancer les Rounds* : Le système génère automatiquement les paires (Système Suisse), 
     (Option G) : Générer un nouveau round (ce charge de generer les round avec la methode suisse)
4.  *Saisir les résultats* : Pour chaque match, vous pouvez :
    * Entrer manuellement le score (1-0, 0-1, 1/2-1/2),
    (Option S): Saisir résultats 
    (Option L): Saisir résultats
5.  *Afficher les Rapports* (Option 3) : Consulter l'état des joueurs et des tournois.
    [1] Liste de tous les joueurs (alphabétique)
[2] Liste de tous les joueurs (par classement)
[3] Liste des tournois
[4] Détails d’un tournoi
[5] Liste des matchs d’un tournoi
[R] Retour
6.  *Sauvegarder les données* (Option 4) : sauvegarde les partie jouer et les enregiste dans la tinydb
7.  *Quitter* (Option Q): Quitte la console