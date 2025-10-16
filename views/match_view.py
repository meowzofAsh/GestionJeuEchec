from typing import Dict, List, Tuple
from models.match_model import MatchModel
from models.joueur_model import JoueurModel


class MatchView:
    """Gère l'affichage des paires de matchs et la saisie des scores."""

    def afficher_saisie_match_actif(
        self, matchs: List[MatchModel], joueurs_ref: Dict[int, JoueurModel]
    ):
        """Affiche les paires pour le round en cours avec le format spécifié."""
        print("\n" + "=" * 25 + " MATCHS ACTUELS " + "=" * 25)

        for i, match in enumerate(matchs):
            j1 = joueurs_ref.get(match.joueur_blanc_id)
            j2 = joueurs_ref.get(match.joueur_noir_id)

            nom_j1 = j1.prenom if j1 else f"Joueur ID {match.joueur_blanc_id}"
            nom_j2 = j2.prenom if j2 else f"Joueur ID {match.joueur_noir_id}"

            print(f"\nMatch #{i+1}:")
            print("┌" + "─" * 40 + "┐")
            print(f"| {nom_j1:^15} vs {nom_j2:^15} |")
            print(
                f"| Score actuel : [{match.score_blanc}] - [{match.score_noir}]"
                + " " * 15
                + "|"
            )
            print("└" + "─" * 40 + "┘")

        print("-" * 67)
        print("[E] Entrer/Modifier un résultat | [C] Clôturer le round | [R] Retour au détail du tournoi")

    def demander_saisie_match(self) -> Tuple[int, str] | None:
        """Demande le numéro du match à saisir et le résultat."""
        print("\n--- Saisie de Résultat ---")
        try:
            match_num = int(input("Numéro du match à saisir : ").strip())
            resultat = input(
                "Entrez le résultat (1-0, 0-1, 0.5-0.5, [J]ouer) : "
            ).strip().upper()
            return (match_num, resultat)
        except ValueError:
            print("Saisie invalide. Le numéro du match doit être un entier.")
            return None

    def get_choice(self) -> str:
        """Demande et retourne le choix de l'utilisateur."""
        return input("Action : ").strip().upper()
