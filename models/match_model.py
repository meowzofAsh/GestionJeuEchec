from typing import Dict, Any


class MatchModel:
    """Modèle représentant un match. Stocke les IDs des joueurs et les scores."""

    def __init__(self, joueur_blanc_id: int, joueur_noir_id: int,
                 score_blanc: float = 0.0, score_noir: float = 0.0):
        self.joueur_blanc_id = joueur_blanc_id
        self.joueur_noir_id = joueur_noir_id
        self.score_blanc = score_blanc
        self.score_noir = score_noir

        # Le stockage sous forme de tuple de deux listes est une contrainte de l'énoncé.
        # On utilise les IDs ici : ([ID_J_Blanc, Score], [ID_J_Noir, Score])
        self.paire_et_scores = (
            [self.joueur_blanc_id, self.score_blanc],
            [self.joueur_noir_id, self.score_noir]
        )

    def serializer(self) -> Dict[str, Any]:
        """Sérialisation pour TinyDB."""
        return {
            'joueur_blanc_id': self.joueur_blanc_id,
            'joueur_noir_id': self.joueur_noir_id,
            'score_blanc': self.score_blanc,
            'score_noir': self.score_noir,
            # Sérialiser la structure exacte demandée (facultatif mais complet)
            'paire_et_scores': self.paire_et_scores
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MatchModel':
        """Désérialisation depuis TinyDB."""
        # On peut reconstruire l'objet à partir des attributs principaux
        return cls(
            joueur_blanc_id=data['joueur_blanc_id'],
            joueur_noir_id=data['joueur_noir_id'],
            score_blanc=data['score_blanc'],
            score_noir=data['score_noir']
        )
