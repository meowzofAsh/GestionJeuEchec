from models.tournois_model import TournoiModel
from typing import List


class TournoiView:
    """Gère l'affichage et la saisie des informations des tournois."""

    def afficher_menu_tournois(self, tournois: List[TournoiModel]):
        """Affiche la liste des tournois actifs."""
        print("\n" + "=" * 7 + " TOURNOIS " + "=" * 7)

        if not tournois:
            print("Aucun tournoi enregistré.")
        else:
            for i, t in enumerate(tournois):
                print(
                    f"{i+1}. {t.nom} | Lieu : {t.lieu} | Tours : {len(t.tours)}/{t.nombre_tours} "
                    f"| Statut : {t.statut}"
                )

        print("-" * 30)
        print("[A] Créer un tournoi")
        print("[V] Voir les détails d’un tournoi")
        print("[R] Retour")

    def afficher_details_tournoi(self, tournoi: TournoiModel):
        """Affiche l'écran 'Détail d’un Tournoi'."""
        print("\n" + "=" * 5 + f" {tournoi.nom.upper()} " + "=" * 5)
        print(f"Lieu : {tournoi.lieu} | Date : {tournoi.date_debut} - {tournoi.date_fin}")
        print(f"Contrôle : {tournoi.controle_temps} | Tours prévus : {tournoi.nombre_tours}")

        print("-" * 40)
        if not tournoi.tours:
            print("Aucun tour n'a encore été généré.")
        else:
            for i, tour in enumerate(tournoi.tours):
                statut = "Terminé" if tour.date_heure_fin else "En cours"
                print(f"{i+1}. {tour.nom} - {statut}")

        print("-" * 40)
        print("[G] Générer un nouveau round")
        print("[S] Saisir résultats")
        print("[L] Liste des joueurs")
        print("[R] Retour")

    def obtenir_choix_tournoi(self) -> int | None:
        """Demande à l'utilisateur quel tournoi voir en détail."""
        try:
            choix = input("Numéro du tournoi à voir (ou R pour retour) : ").strip().upper()
            if choix == "R":
                return None
            return int(choix)
        except ValueError:
            print("Saisie invalide. Veuillez entrer un numéro.")
            return None

    def get_user_choice(self) -> str:
        """Demande et retourne le choix de l'utilisateur."""
        return input("Votre choix : ").strip().upper()
