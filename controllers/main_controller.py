from views.menu_view import MenuView
from services.stockage_service import StockageService
from controllers.joueur_controller import JoueurController
from controllers.tournois_controller import TournoiController
from controllers.rapport_controller import RapportController


class MainController:
    """Contrôleur principal gérant le flux du programme."""

    def __init__(self):
        self.menu_view = MenuView()
        self.stockage_service = StockageService()

        # Initialisation des sous-contrôleurs
        self.joueur_controller = JoueurController(self.stockage_service)
        self.tournoi_controller = TournoiController(self.stockage_service)
        self.rapport_controller = RapportController(self.stockage_service)

    def run(self):
        """Lance la boucle principale de l'application."""

        # Tente de charger les données au démarrage
        statut = self.charger_et_mettre_a_jour_statut()

        running = True
        while running:
            self.menu_view.display_main_menu(statut_sauvegarde=statut)
            choice = self.menu_view.get_user_choice()

            if choice == '1':
                self.joueur_controller.gerer_joueurs()
                statut = self.sauvegarder_et_mettre_a_jour_statut()
            elif choice == '2':
                self.tournoi_controller.gerer_tournois()
                statut = self.sauvegarder_et_mettre_a_jour_statut()
            elif choice == '3':
                self.rapport_controller.gerer_rapports()
                print(">>> Action : Rapports (À IMPLÉMENTER)")
            elif choice == '4':
                statut = self.sauvegarder_et_mettre_a_jour_statut()
            elif choice == '5':
                statut = self.charger_et_mettre_a_jour_statut()
            elif choice == 'Q':
                running = False
            else:
                print("Choix invalide. Veuillez réessayer.")

        print("Programme terminé. Au revoir !")

    def sauvegarder_et_mettre_a_jour_statut(self) -> str:
        """Sauvegarde les données et retourne un message de statut."""
        try:
            self.stockage_service.sauvegarder_donnees()
            return "Sauvegarde OK"
        except Exception as e:
            return f"Sauvegarde ERREUR: {e}"

    def charger_et_mettre_a_jour_statut(self) -> str:
        """Charge les données et retourne un message de statut."""
        try:
            self.stockage_service.charger_donnees()
            return "Chargement OK"
        except Exception as e:
            return f"Chargement ERREUR: {e}"
