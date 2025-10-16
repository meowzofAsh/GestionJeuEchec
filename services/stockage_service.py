from tinydb import TinyDB
from typing import List
from models.joueur_model import JoueurModel
from models.tournois_model import TournoiModel


class StockageService:
    """Gère la persistance des données Joueurs et Tournois via TinyDB."""

    def __init__(self, db_path='db.json'):
        self.db_path = db_path
        self.db = TinyDB(db_path)
        self.joueurs_table = self.db.table('joueurs')
        self.tournois_table = self.db.table('tournois')

        # Stockage en mémoire des instances après chargement
        self.joueurs_en_memoire: List[JoueurModel] = []
        self.tournois_en_memoire: List[TournoiModel] = []

        # ID max pour simuler l'auto-incrémentation
        self.max_joueur_id = 0
        self.max_tournoi_id = 0

    # --- Chargement et Désérialisation ---

    def charger_joueurs(self) -> List[JoueurModel]:
        """Charge et désérialise tous les joueurs."""
        self.joueurs_en_memoire = []
        self.max_joueur_id = 0

        for data in self.joueurs_table.all():
            joueur = JoueurModel.from_dict(data)
            self.joueurs_en_memoire.append(joueur)
            if joueur.joueur_id is not None and joueur.joueur_id > self.max_joueur_id:
                self.max_joueur_id = joueur.joueur_id

        return self.joueurs_en_memoire

    def charger_tournois(self) -> List[TournoiModel]:
        """Charge et désérialise tous les tournois."""
        self.tournois_en_memoire = []
        self.max_tournoi_id = 0

        for data in self.tournois_table.all():
            tournoi = TournoiModel.from_dict(data)
            self.tournois_en_memoire.append(tournoi)
            if tournoi.tournoi_id is not None and tournoi.tournoi_id > self.max_tournoi_id:
                self.max_tournoi_id = tournoi.tournoi_id

        return self.tournois_en_memoire

    def charger_donnees(self):
        """Charge l'état complet du programme."""
        self.charger_joueurs()
        self.charger_tournois()
        # TinyDB gère automatiquement la lecture, pas besoin de réouvrir

    # --- Sauvegarde et Sérialisation ---

    def _attribuer_ids(self):
        """Attribue les IDs aux joueurs et tournois si nécessaire (au moment de la sauvegarde)."""
        for joueur in self.joueurs_en_memoire:
            if joueur.joueur_id is None:
                self.max_joueur_id += 1
                joueur.joueur_id = self.max_joueur_id

        for tournoi in self.tournois_en_memoire:
            if tournoi.tournoi_id is None:
                self.max_tournoi_id += 1
                tournoi.tournoi_id = self.max_tournoi_id

    def sauvegarder_joueurs(self):
        """Sauvegarde les joueurs sérialisés."""
        self.joueurs_table.truncate()
        serialized_joueurs = [j.serializer() for j in self.joueurs_en_memoire]
        if serialized_joueurs:
            self.joueurs_table.insert_multiple(serialized_joueurs)

    def sauvegarder_tournois(self):
        """Sauvegarde les tournois sérialisés."""
        self.tournois_table.truncate()
        serialized_tournois = [t.serializer() for t in self.tournois_en_memoire]
        if serialized_tournois:
            self.tournois_table.insert_multiple(serialized_tournois)

    def sauvegarder_donnees(self):
        """Sauvegarde l'état complet du programme."""
        self._attribuer_ids()
        self.sauvegarder_joueurs()
        self.sauvegarder_tournois()
        self.db.close()

    # --- Utilitaires d'attribution d'ID ---

    def attribuer_id_joueur(self, joueur: JoueurModel):
        """Attribue le prochain ID séquentiel disponible à un joueur."""
        if joueur.joueur_id is None:
            self.max_joueur_id += 1
            joueur.joueur_id = self.max_joueur_id

    def attribuer_id_tournoi(self, tournoi: TournoiModel):
        """Attribue le prochain ID séquentiel disponible à un tournoi."""
        if tournoi.tournoi_id is None:
            self.max_tournoi_id += 1
            tournoi.tournoi_id = self.max_tournoi_id

    # --- Utilitaires de Recherche ---

    def obtenir_joueur_par_id(self, joueur_id: int) -> JoueurModel | None:
        """Récupère une instance Joueur en mémoire par son ID."""
        for joueur in self.joueurs_en_memoire:
            if joueur.joueur_id == joueur_id:
                return joueur
        return None
