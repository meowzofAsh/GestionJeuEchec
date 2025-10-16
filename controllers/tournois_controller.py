from datetime import datetime
from services.stockage_service import StockageService
from models.tournois_model import TournoiModel
from models.tours_model import TourModel
from views.tournois_view import TournoiView
from controllers.appariement_controller import AppariementController
from controllers.match_controller import MatchController


class TournoiController:
    """Gère la création, la visualisation et le flux des tournois."""

    def __init__(self, stockage_service: StockageService):
        self.stockage = stockage_service
        self.tournoi_view = TournoiView()
        self.appariement_controller = AppariementController(stockage_service)
        self.match_controller = MatchController(stockage_service)  # Utilisation du nouveau contrôleur

    def gerer_tournois(self):
        """Boucle principale de la gestion des tournois."""
        running = True
        while running:
            tournois = self.stockage.tournois_en_memoire
            self.tournoi_view.afficher_menu_tournois(tournois)
            choice = self.tournoi_view.get_user_choice()

            if choice == 'A':
                self.creer_tournoi()
            elif choice == 'V':
                self.visualiser_tournoi_detail()
            elif choice == 'R':
                running = False
            else:
                print("Choix invalide.")

    def creer_tournoi(self):
        """Simule la création d'un tournoi (nécessite 8 joueurs)."""
        if len(self.stockage.joueurs_en_memoire) < 8:
            print("Erreur : Il faut au moins 8 joueurs enregistrés pour créer un tournoi.")
            return

        joueurs_ids = [j.joueur_id for j in self.stockage.joueurs_en_memoire[:8]]

        nouveau_tournoi = TournoiModel(
            nom="Open du Week-end",
            lieu="Cocody",
            date_debut="2025-10-15",
            date_fin="2025-10-15",
            controle_temps="Blitz",
            description="Tournoi test",
            joueurs_ids=joueurs_ids,
        )
        self.stockage.tournois_en_memoire.append(nouveau_tournoi)
        print(f"Tournoi '{nouveau_tournoi.nom}' créé avec 8 joueurs.")

    def visualiser_tournoi_detail(self):
        """Affiche les détails d'un tournoi et gère les actions du tour en cours."""
        tournois = self.stockage.tournois_en_memoire
        choix_index = self.tournoi_view.obtenir_choix_tournoi()

        if choix_index is None:
            return

        try:
            tournoi = tournois[choix_index - 1]
        except IndexError:
            print("Numéro de tournoi invalide.")
            return

        running = True
        while running:
            self.tournoi_view.afficher_details_tournoi(tournoi)
            choice = self.tournoi_view.get_user_choice()

            if choice == 'G':
                self.generer_nouveau_tour(tournoi)
            elif choice == 'S':
                # Délégué au contrôleur de match
                self.match_controller.saisir_resultats_et_cloturer(tournoi)
            elif choice == 'L':
                print(">>> Action : Liste des joueurs du tournoi (Rapport à implémenter)")
            elif choice == 'R':
                running = False
            else:
                print("Choix invalide.")

    def generer_nouveau_tour(self, tournoi: TournoiModel):
        """Génère un nouveau TourModel et ses appariements (logique Suisse)."""
        if tournoi.statut == "Terminé" or (
            tournoi.tours and tournoi.tours[-1].date_heure_fin is None
        ):
            print("Erreur : Tournoi terminé ou tour précédent non clôturé.")
            return

        tour_actuel_num = len(tournoi.tours) + 1
        if tour_actuel_num > tournoi.nombre_tours:
            print(f"Erreur : Le nombre maximum de tours ({tournoi.nombre_tours}) est atteint.")
            return

        nom_tour = f"Round {tour_actuel_num}"
        matchs = self.appariement_controller.generer_appariements(
            tournoi.joueurs_ids,
            tour_actuel_num,
        )

        nouveau_tour = TourModel(
            nom=nom_tour,
            matchs=matchs,
            date_heure_debut=datetime.now(),
        )
        tournoi.tours.append(nouveau_tour)
        print(f"Nouveau tour '{nom_tour}' généré avec succès.")
