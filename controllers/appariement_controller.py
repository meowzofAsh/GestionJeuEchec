from typing import List
from models.match_model import MatchModel


class AppariementController:
    """Implémente la logique d'appariement du système suisse."""

    def __init__(self, stockage_service):
        self.stockage = stockage_service

    def generer_appariements(self, joueurs_ids: List[int], tour_actuel: int) -> List[MatchModel]:
        """
        Génère la liste des matchs pour le tour spécifié selon le système suisse.
        :param joueurs_ids: Liste des IDs des joueurs dans le tournoi.
        :param tour_actuel: Le numéro du tour (1 pour Round 1, 2 pour Round 2, etc.).
        :return: Liste des instances MatchModel.
        """
        # 1. Récupérer les instances complètes des joueurs
        joueurs = [self.stockage.obtenir_joueur_par_id(pid) for pid in joueurs_ids]

        # Filtrer les IDs invalides (juste au cas où)
        joueurs = [j for j in joueurs if j is not None]

        # 2. Trier les joueurs selon les règles
        if tour_actuel == 1:
            # R1 : Trier par CLASSEMENT
            joueurs_tries = sorted(joueurs, key=lambda j: j.classement, reverse=True)
        else:
            # R2+ : Trier par POINTS, puis par CLASSEMENT
            def critere_tri(joueur):
                return (-joueur.points_totaux, -joueur.classement)  # Décroissant

            joueurs_tries = sorted(joueurs, key=critere_tri)

        # 3. Procéder au jumelage
        matchs = []
        joueurs_disponibles = list(joueurs_tries)

        while joueurs_disponibles:
            j1 = joueurs_disponibles.pop(0)  # Toujours prendre le meilleur disponible

            adversaire_trouve = False
            for i, j2 in enumerate(joueurs_disponibles):

                if tour_actuel == 1:
                    if (
                        len(joueurs_tries) == 8
                        and j2.joueur_id
                        == joueurs_tries[4 + joueurs_tries.index(j1)].joueur_id
                    ):
                        pass

                # Condition principale : Les joueurs ne doivent pas avoir déjà joué ensemble
                if j2.joueur_id not in j1.adversaires_rencontres:
                    # Jumelage trouvé !
                    matchs.append(MatchModel(j1.joueur_id, j2.joueur_id))
                    joueurs_disponibles.pop(i)
                    # Retirer l'adversaire de la liste
                    adversaire_trouve = True
                    break

            if not adversaire_trouve:
                # Gestion du cas où le joueur n'a pas d'adversaire légitime (par exemple, s'il a joué contre tous)
                # La spécification ne donne pas de règle pour la gestion des "flottants" (pairings floats)
                # S'il ne reste qu'un seul joueur, il reçoit un "Bye" (non implémenté ici car N joueurs = 8)
                print(f"ALERTE : pair difficile pour le joueur ID {j1.joueur_id}. Tentative de forcer l'appariement.")
                # Pour cet exercice, nous allons forcer un appariement avec le prochain joueur disponible
                # (méthode simple par défaut), même s'ils ont déjà joué, pour éviter le blocage.
                # (Dans une implémentation réelle, on testerait P3, P4, etc.)
                if joueurs_disponibles:
                    j2 = joueurs_disponibles.pop(0)
                    print(f"Jumelage forcé : J{j1.joueur_id} vs J{j2.joueur_id}.")
                    matchs.append(MatchModel(j1.joueur_id, j2.joueur_id))
                else:
                    # Ne devrait pas arriver avec 8 joueurs.
                    print(f"Erreur : Impossible de trouver un adversaire pour J{j1.joueur_id}. Le joueur est ignoré.")

        return matchs
