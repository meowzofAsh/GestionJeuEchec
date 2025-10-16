from models.joueur_model import JoueurModel
from views.joueur_view import JoueurView
from services.stockage_service import StockageService


class JoueurController:
    """Gère la logique métier des joueurs (ajout, modification, affichage)."""

    def __init__(self, stockage_service: StockageService):
        self.stockage = stockage_service
        self.joueur_view = JoueurView()

    def gerer_joueurs(self):
        """Boucle principale pour le menu des joueurs."""
        running = True
        while running:
            joueurs = self.stockage.joueurs_en_memoire
            self.joueur_view.afficher_menu_joueurs(joueurs)
            choice = self.joueur_view.get_user_choice()

            if choice == 'A':
                self.ajouter_joueur()
            elif choice == 'M':
                self.modifier_classement()
            elif choice == 'T':
                # Afficher trié (logique simple ici, trié par nom de famille)
                joueurs_tries = sorted(joueurs, key=lambda j: j.nom_famille)
                self.joueur_view.afficher_liste_joueurs_trie(
                    joueurs_tries, "Liste triée par Nom"
                )
            elif choice == 'R':
                running = False
            else:
                print("Choix invalide.")

    def ajouter_joueur(self):
        """Récupère les données via la vue et crée une instance JoueurModel."""
        try:
            # Assurez-vous que la méthode dans JoueurView s'appelle bien saisir_nouveau_joueur
            data = self.joueur_view.saisir_nouveau_joueur()
            if not data:
                return

            nouveau_joueur = JoueurModel(**data)

            # --- CORRECTION DE L'ERREUR D'AFFICHAGE (Attribution de l'ID en mémoire) ---
            self.stockage.attribuer_id_joueur(nouveau_joueur)
            # ---------------------------------------------------------------------------

            self.stockage.joueurs_en_memoire.append(nouveau_joueur)
            print(
                f"\nJoueur {nouveau_joueur.prenom} {nouveau_joueur.nom_famille} "
                f"ajouté en mémoire avec l'ID {nouveau_joueur.joueur_id}"
            )

        except ValueError as e:
            print(f"Erreur de saisie : {e}")

    def modifier_classement(self):
        """Gère la modification du classement d'un joueur existant."""
        # Logique de modification à implémenter si ce n'est pas fait
        print("Fonction de modification de classement non encore implémentée.")
