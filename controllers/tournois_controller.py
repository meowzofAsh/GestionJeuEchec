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
        """Créer un nouveau tournoi en utilisant la saisie utilisateur."""
        # 1. Obtient les données du tournoi via la vue
        donnees_tournoi = self.tournoi_view.saisir_nouveau_tournoi()
        if donnees_tournoi is None:
            # Saisie annulée
            return

        # 2. Vérifie qu'il y a assez de joueurs (8 requis pour le moment)
        if len(self.stockage.joueurs_en_memoire) < 8:
            print("Erreur : Il faut au moins 8 joueurs enregistrés pour créer un tournoi.")
            return

        # 3. Sélectionne les 8 premiers joueurs (méthode temporaire)
        joueurs_ids = [j.joueur_id for j in self.stockage.joueurs_en_memoire[:8]]

        # 4. Crée l'instance TournoiModel avec les données saisies
        nouveau_tournoi = TournoiModel(
            nom=donnees_tournoi["nom"],
            lieu=donnees_tournoi["lieu"],
            date_debut=donnees_tournoi["date_debut"],
            date_fin=donnees_tournoi["date_fin"],
            controle_temps=donnees_tournoi["controle_temps"],
            description=donnees_tournoi["description"],
            nombre_tours=donnees_tournoi["nombre_tours"],  # Ajout pour initialiser
            joueurs_ids=joueurs_ids,
        )

        # 5. Attribue un ID (si vous avez implémenté attribuer_id_tournoi dans StockageService)
        # S'il manque, assurez-vous de l'ajouter pour la gestion des IDs
        if hasattr(self.stockage, 'attribuer_id_tournoi'):
            self.stockage.attribuer_id_tournoi(nouveau_tournoi)

        # 6. Ajoute le tournoi en mémoire
        self.stockage.tournois_en_memoire.append(nouveau_tournoi)
        print(f"Tournoi '{nouveau_tournoi.nom}' créé avec {len(joueurs_ids)} joueurs.")

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

        try:
            matchs = self.appariement_controller.generer_appariements(
                tournoi.joueurs_ids,
                tour_actuel_num,
            )
        except ValueError as e:
            print(f"Erreur d'appariement : {e}")
            return

        nouveau_tour = TourModel(
            nom=nom_tour,
            matchs=matchs,
            date_heure_debut=datetime.now(),
        )
        tournoi.tours.append(nouveau_tour)
        print(f"Nouveau tour '{nom_tour}' généré avec succès.")
