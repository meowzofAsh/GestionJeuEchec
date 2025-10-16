from datetime import datetime


class MenuView:
    """Gère l'affichage du menu principal et la saisie des choix."""

    def __init__(self):
        # La date sera mise à jour dynamiquement
        self.date_du_jour = datetime.now().strftime("%d %B %Y")

    def display_main_menu(self, statut_sauvegarde: str = "Inconnu"):
        """Affiche le menu principal de la console."""
        # Mettre à jour la date à chaque affichage
        self.date_du_jour = datetime.now().strftime("%d %B %Y")

        print("\n" + "=" * 41)
        print(" " * 6 + "GESTION TOURNOI SYSTÈME SUISSE")
        print("=" * 41)

        # Formatage des informations de date et sauvegarde
        info_ligne = f"Date : {self.date_du_jour}"
        info_ligne += " " * (
            40 - len(info_ligne) - len(f"État : {statut_sauvegarde}")
        )
        info_ligne += f"État : {statut_sauvegarde}"
        print(info_ligne)
        print("-" * 41)

        print("\n[1] Gérer les joueurs")
        print("[2] Gérer les tournois")
        print("[3] Rapports")
        print("[4] Sauvegarder les données")
        print("[5] Charger les données")
        print("[Q] Quitter")
        print("-" * 41)

    def get_user_choice(self) -> str:
        """Demande et retourne le choix de l'utilisateur."""
        return input("Votre choix : ").strip().upper()
