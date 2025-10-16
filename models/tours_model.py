from datetime import datetime
from typing import List, Dict, Any
from .match_model import MatchModel


class TourModel:
    """Modèle représentant un tour (Round) dans le tournoi."""

    def __init__(
        self,
        nom: str,
        matchs: List[MatchModel] = None,
        date_heure_debut: datetime = None,
        date_heure_fin: datetime = None
    ):
        self.nom = nom
        self.matchs = matchs if matchs is not None else []
        self.date_heure_debut = date_heure_debut
        self.date_heure_fin = date_heure_fin

    def serializer(self) -> Dict[str, Any]:
        """Sérialisation pour TinyDB (inclut la sérialisation des matchs)."""
        return {
            'nom': self.nom,
            # Convertir les datetimes en chaînes ISO pour la persistance
            'date_heure_debut': self.date_heure_debut.isoformat() if self.date_heure_debut else None,
            'date_heure_fin': self.date_heure_fin.isoformat() if self.date_heure_fin else None,
            # Sérialiser chaque match
            'matchs': [match.serializer() for match in self.matchs],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TourModel':
        """Désérialisation depuis TinyDB (inclut la désérialisation des matchs)."""
        matchs_deser = [MatchModel.from_dict(m) for m in data.get('matchs', [])]

        # Reconvertir les chaînes en objets datetime
        debut = datetime.fromisoformat(data['date_heure_debut']) if data['date_heure_debut'] else None
        fin = datetime.fromisoformat(data['date_heure_fin']) if data['date_heure_fin'] else None

        return cls(
            nom=data['nom'],
            matchs=matchs_deser,
            date_heure_debut=debut,
            date_heure_fin=fin,
        )
