from datetime import date
from typing import List, Dict, Any


class JoueurModel:
    """Modèle représentant un joueur d'échecs."""

    def __init__(
        self,
        nom_famille: str,
        prenom: str,
        date_naissance: date,
        sexe: str,
        classement: int,
        joueur_id: int = None,
        points_totaux: float = 0.0,
        adversaires_rencontres: List[int] = None,
    ):
        self.joueur_id = joueur_id
        self.nom_famille = nom_famille
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.sexe = sexe
        self.classement = classement
        self.points_totaux = points_totaux

        # Liste des IDs des joueurs rencontrés (pour le système suisse)
        self.adversaires_rencontres = (
            adversaires_rencontres if adversaires_rencontres is not None else []
        )

    # --- Méthodes de Persistance (Sérialisation / Désérialisation) ---

    def serializer(self) -> Dict[str, Any]:
        """Convertit l'instance en dictionnaire pour TinyDB."""
        return {
            "joueur_id": self.joueur_id,
            "nom_famille": self.nom_famille,
            "prenom": self.prenom,
            # Conversion de l'objet date en chaîne de caractères ISO
            "date_naissance": self.date_naissance.isoformat(),
            "sexe": self.sexe,
            "classement": self.classement,
            "points_totaux": self.points_totaux,
            "adversaires_rencontres": self.adversaires_rencontres,
        }

    @classmethod
    def from_dict(cls, joueur_data: Dict[str, Any]) -> "JoueurModel":
        """Crée une instance à partir d'un dictionnaire de TinyDB."""
        try:
            date_obj = date.fromisoformat(joueur_data["date_naissance"])
        except ValueError:
            date_obj = date(1900, 1, 1)  # Valeur par défaut si format invalide

        return cls(
            joueur_id=joueur_data.get("joueur_id"),
            nom_famille=joueur_data["nom_famille"],
            prenom=joueur_data["prenom"],
            date_naissance=date_obj,
            sexe=joueur_data["sexe"],
            classement=joueur_data["classement"],
            points_totaux=joueur_data.get("points_totaux", 0.0),
            adversaires_rencontres=joueur_data.get("adversaires_rencontres", []),
        )
