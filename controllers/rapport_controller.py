from typing import List
from models.tournois_model import TournoiModel
from services.stockage_service import StockageService
from views.rapport_view import RapportView
from models.joueur_model import JoueurModel


class RapportController:
    """Gère la génération des différents rapports demandés."""

    def __init__(self, stockage_service: StockageService):
        self.stockage = stockage_service
        self.rapport_view = RapportView()

    def gerer_rapports(self):
        """Boucle principale pour le menu des rapports."""
        running = True
        while running:
            self.rapport_view.afficher_menu_rapports()
            choice = self.rapport_view.get_user_choice()

            joueurs = self.stockage.joueurs_en_memoire
            tournois = self.stockage.tournois_en_memoire

            if choice == '1':
                self.afficher_joueurs_alphabetique(joueurs)
            elif choice == '2':
                self.afficher_joueurs_par_classement(joueurs)
            elif choice == '3':
                self.rapport_view.afficher_liste_tournois(tournois)
            elif choice == '4':
                self.afficher_details_tournoi(tournois)
            elif choice == '5':
                self.afficher_matchs_tournoi(tournois)
            elif choice == 'R':
                running = False
            else:
                print("Choix invalide.")

    def afficher_joueurs_alphabetique(self, joueurs: List[JoueurModel]):
        """Affiche les joueurs triés par nom de famille."""
        joueurs_tries = sorted(joueurs, key=lambda j: j.nom_famille)
        self.rapport_view.afficher_liste_joueurs(
            joueurs_tries, "Tous les joueurs (Alphabétique)"
        )

    def afficher_joueurs_par_classement(self, joueurs: List[JoueurModel]):
        """Affiche les joueurs triés par classement."""
        # Tri descendant (meilleur classement en premier)
        joueurs_tries = sorted(joueurs, key=lambda j: j.classement, reverse=True)
        self.rapport_view.afficher_liste_joueurs(
            joueurs_tries, "Tous les joueurs (Par Classement)"
        )

    def afficher_details_tournoi(self, tournois: List[TournoiModel]):
        """Affiche les détails complets d'un seul tournoi (délégué à TournoiView)."""
        self.rapport_view.afficher_liste_tournois(tournois)
        choix_index = self.rapport_view.obtenir_choix_tournoi()

        if choix_index is not None and 0 < choix_index <= len(tournois):
            # On utilise ici la vue de rapport pour afficher les détails du tournoi
            # (pour rester dans le contexte des rapports).
            tournoi = tournois[choix_index - 1]
            print(f"\n--- Détails du Tournoi : {tournoi.nom} ---")
            print(f"Description : {tournoi.description}")
            # La TournoiView peut être réutilisée pour un affichage plus riche si nécessaire.
        else:
            print("Sélection annulée ou invalide.")

    def afficher_matchs_tournoi(self, tournois: List[TournoiModel]):
        """Affiche tous les matchs joués d'un tournoi sélectionné."""
        self.rapport_view.afficher_liste_tournois(tournois)
        choix_index = self.rapport_view.obtenir_choix_tournoi()

        if choix_index is not None and 0 < choix_index <= len(tournois):
            tournoi = tournois[choix_index - 1]
            # Créer un dictionnaire de référence ID -> Joueur pour l'affichage des noms
            joueurs_ref = {j.joueur_id: j for j in self.stockage.joueurs_en_memoire}
            self.rapport_view.afficher_matchs_tournoi(tournoi, joueurs_ref)
        else:
            print("Sélection annulée ou invalide.")
