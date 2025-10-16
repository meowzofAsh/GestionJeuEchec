from typing import List, Dict, Any
from .tours_model import TourModel


class TournoiModel:
    """Modèle représentant un tournoi d'échecs."""

    def __init__(self, nom: str, lieu: str, date_debut: str, date_fin: str,
                 controle_temps: str, description: str,
                 nombre_tours: int = 4, tournoi_id: int = None,
                 joueurs_ids: List[int] = None, tours: List[TourModel] = None):
        self.tournoi_id = tournoi_id
        self.nom = nom
        self.lieu = lieu
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.nombre_tours = nombre_tours
        self.controle_temps = controle_temps
        self.description = description

        # Stocke les IDs des joueurs participants
        self.joueurs_ids = joueurs_ids if joueurs_ids is not None else []
        self.tours = tours if tours is not None else []

    # ... (Méthodes de sérialisation et désérialisation à implémenter.)
    @property
    def statut(self) -> str:
        """Retourne le statut actuel du tournoi (En cours, Terminé, En attente)."""
        if not self.tours:
            return "En attente"
        elif len(self.tours) == self.nombre_tours and \
                self.tours[-1].date_heure_fin is not None:
            return "Terminé"
        else:
            return "En cours"

    def serializer(self) -> Dict[str, Any]:
        """Sérialisation pour TinyDB (inclut la sérialisation des tours)."""
        return {
            'tournoi_id': self.tournoi_id,
            'nom': self.nom,
            'lieu': self.lieu,
            'date_debut': self.date_debut,  # Stocké en str (AAAA-MM-JJ)
            'date_fin': self.date_fin,
            'nombre_tours': self.nombre_tours,
            'controle_temps': self.controle_temps,
            'description': self.description,
            'joueurs_ids': self.joueurs_ids,
            # Sérialiser chaque tour
            'tours': [tour.serializer() for tour in self.tours]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TournoiModel':
        """Désérialisation depuis TinyDB (inclut la désérialisation des tours)."""
        tours_deser = [TourModel.from_dict(t) for t in data.get('tours', [])]

        return cls(
            tournoi_id=data.get('tournoi_id'),
            nom=data['nom'],
            lieu=data['lieu'],
            date_debut=data['date_debut'],
            date_fin=data['date_fin'],
            nombre_tours=data['nombre_tours'],
            controle_temps=data['controle_temps'],
            description=data['description'],
            joueurs_ids=data.get('joueurs_ids', []),
            tours=tours_deser
        )
