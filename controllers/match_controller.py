from datetime import datetime
from models.tournois_model import TournoiModel


class MatchController:
    """Gère la saisie des résultats pour un tour."""

    def __init__(self, stockage_service):
        self.stockage = stockage_service

    def saisir_resultats_et_cloturer(self, tournoi: TournoiModel):
        """Logique de saisie des scores et mise à jour des points/adversaires."""
        if not tournoi.tours or tournoi.tours[-1].date_heure_fin is not None:
            print("Aucun tour en cours à saisir.")
            return

        tour_en_cours = tournoi.tours[-1]
        print(f"\n--- SAISIE DES RÉSULTATS : {tour_en_cours.nom} ---")

        for match in tour_en_cours.matchs:
            # Récupérer les objets Joueur
            j1 = self.stockage.obtenir_joueur_par_id(match.joueur_blanc_id)
            j2 = self.stockage.obtenir_joueur_par_id(match.joueur_noir_id)

            # Saisie via input
            resultat_str = input(
                f"Résultat pour {j1.prenom} vs {j2.prenom} (1-0, 0-1, 0.5-0.5) : "
            ).strip()

            score_b, score_n = 0.0, 0.0
            if resultat_str == "1-0":
                score_b, score_n = 1.0, 0.0
            elif resultat_str == "0-1":
                score_b, score_n = 0.0, 1.0
            elif resultat_str in ("0.5-0.5", "1/2-1/2"):
                score_b, score_n = 0.5, 0.5
            else:
                print("Résultat non reconnu. Match ignoré pour l'instant.")
                continue

            # Mise à jour des modèles
            match.score_blanc = score_b
            match.score_noir = score_n
            j1.points_totaux += score_b
            j2.points_totaux += score_n
            j1.adversaires_rencontres.append(j2.joueur_id)
            j2.adversaires_rencontres.append(j1.joueur_id)
            print(f"Scores enregistrés : {j1.prenom} ({score_b}) vs {j2.prenom} ({score_n})")

        # Clôturer le tour
        tour_en_cours.date_heure_fin = datetime.now()
        print(f"\n--- Le tour '{tour_en_cours.nom}' est CLÔTURÉ et les points ont été mis à jour.")

        if tournoi.statut == "Terminé":
            print("\n!!! Le tournoi est TERMINÉ !!!")
