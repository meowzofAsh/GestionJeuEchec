from typing import List
from models.match_model import MatchModel
from services.stockage_service import StockageService


class AppariementController:
    """Gère la logique d'appariement des joueurs selon le système suisse."""

    def __init__(self, stockage_service: StockageService):
        self.stockage = stockage_service

    def generer_appariements(self, joueurs_ids: List[int], tour_actuel_num: int) -> List[MatchModel]:
        """
        Génère les paires de matchs pour le tour actuel.

        Pour le Tour 1 : appariement selon le classement (top moitié vs bottom moitié).
        Pour les tours suivants : appariement selon les points puis le classement.
        """
        if len(joueurs_ids) % 2 != 0:
            raise ValueError("Le nombre de joueurs doit être pair pour l'appariement.")

        # 1️⃣ Récupérer les objets Joueur à partir de leurs IDs
        joueurs_objets = [self.stockage.obtenir_joueur_par_id(j_id) for j_id in joueurs_ids]
        joueurs_objets = [j for j in joueurs_objets if j is not None]

        # 2️⃣ Trier les joueurs selon le tour
        if tour_actuel_num == 1:
            # Tour 1 : classement croissant (1 = meilleur)
            joueurs_tries = sorted(joueurs_objets, key=lambda j: j.classement)
        else:
            # Tours suivants : points totaux décroissants, puis classement croissant
            joueurs_tries = sorted(
                joueurs_objets,
                key=lambda j: (j.points_totaux, -j.classement),
                reverse=True
            )

        matchs: List[MatchModel] = []
        n = len(joueurs_tries)
        moitie = n // 2

        # 3️⃣ Logique d'appariement
        if tour_actuel_num == 1:
            # Top Half vs Bottom Half
            for i in range(moitie):
                j1 = joueurs_tries[i]
                j2 = joueurs_tries[i + moitie]

                match = MatchModel(
                    joueur_blanc_id=j1.joueur_id,
                    joueur_noir_id=j2.joueur_id
                )
                matchs.append(match)

        else:
            # Tours suivants : simple appariement par ordre de tri (à améliorer plus tard)
            for i in range(0, n, 2):
                j1 = joueurs_tries[i]
                j2 = joueurs_tries[i + 1]

                match = MatchModel(
                    joueur_blanc_id=j1.joueur_id,
                    joueur_noir_id=j2.joueur_id
                )
                matchs.append(match)

        return matchs
