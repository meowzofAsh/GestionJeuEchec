from typing import List, Dict
from models.joueur_model import JoueurModel
from models.tournois_model import TournoiModel


class RapportView:
    """Gère l'affichage du menu des rapports et le formatage des données des rapports."""

    def afficher_menu_rapports(self):
        """Affiche le menu de sélection des rapports."""
        print("\n" + "=" * 5 + " RAPPORTS " + "=" * 5)
        print("[1] Liste de tous les joueurs (alphabétique)")
        print("[2] Liste de tous les joueurs (par classement)")
        print("[3] Liste des tournois")
        print("[4] Détails d’un tournoi")
        print("[5] Liste des matchs d’un tournoi")
        print("[R] Retour")
        print("-" * 20)

    def afficher_liste_joueurs(self, joueurs: List[JoueurModel], titre: str):
        """Affiche une liste de joueurs selon un critère donné."""
        print(f"\n===== {titre.upper()} =====")
        print("ID | NOM | PRÉNOM | CLASSEMENT | POINTS | DATE DE NAISSANCE")
        print("-" * 75)

        if not joueurs:
            print("Aucun joueur trouvé.")
        else:
            for joueur in joueurs:
                dob_str = joueur.date_naissance.strftime("%Y-%m-%d")
                print(
                    f"{joueur.joueur_id:<2} | {joueur.nom_famille:<4} | {joueur.prenom:<6} "
                    f"| {joueur.classement:<10} | {joueur.points_totaux:<6} | {dob_str}"
                )
        print("-" * 75)

    def afficher_liste_tournois(self, tournois: List[TournoiModel]):
        """Affiche une liste simple de tous les tournois."""
        print("\n===== LISTE DES TOURNOIS =====")

        if not tournois:
            print("Aucun tournoi enregistré.")
            return

        for i, t in enumerate(tournois):
            print(
                f"{i+1}. {t.nom} | Lieu : {t.lieu} | Tours : {len(t.tours)}/{t.nombre_tours} "
                f"| Statut : {t.statut}"
            )
        print("-" * 35)

    def afficher_matchs_tournoi(
        self, tournoi: TournoiModel, joueurs_ref: Dict[int, JoueurModel]
    ):
        """Affiche les matchs joués pour tous les tours d'un tournoi."""
        print(f"\n===== MATCHS DU TOURNOI : {tournoi.nom.upper()} =====")

        if not tournoi.tours:
            print("Aucun tour n'a été joué.")
            return

        for i, tour in enumerate(tournoi.tours):
            statut = "Terminé" if tour.date_heure_fin else "En cours"
            print(f"\n--- {tour.nom} ({statut}) ---")

            for match in tour.matchs:
                j1 = joueurs_ref.get(match.joueur_blanc_id)
                j2 = joueurs_ref.get(match.joueur_noir_id)

                nom_j1 = j1.prenom if j1 else f"ID {match.joueur_blanc_id}"
                nom_j2 = j2.prenom if j2 else f"ID {match.joueur_noir_id}"

                score_aff = f"[{match.score_blanc}] - [{match.score_noir}]"
                print(
                    f"Match : {nom_j1} ({j1.points_totaux} pts) vs {nom_j2} ({j2.points_totaux} pts) "
                    f"| Score : {score_aff}"
                )

    def get_user_choice(self) -> str:
        """Demande et retourne le choix de l'utilisateur."""
        return input("Votre choix : ").strip().upper()

    def obtenir_choix_tournoi(self) -> int | None:
        """Demande à l'utilisateur quel tournoi sélectionner (pour les détails)."""
        try:
            choix = input("Numéro du tournoi : ").strip()
            return int(choix)
        except ValueError:
            print("Saisie invalide. Veuillez entrer un numéro.")
            return None
