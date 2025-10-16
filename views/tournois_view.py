from models.tournois_model import TournoiModel
from typing import List
from datetime import date


class TournoiView:
    """Gère l'affichage et la saisie des informations des tournois."""

    def afficher_menu_tournois(self, tournois: List[TournoiModel]):
        """Affiche la liste des tournois actifs."""
        print("\n" + "=" * 7 + " TOURNOIS " + "=" * 7)

        if not tournois:
            print("Aucun tournoi enregistré.")
        else:
            for i, t in enumerate(tournois):
                print(
                    f"{i+1}. {t.nom} | Lieu : {t.lieu} | Tours : {len(t.tours)}/{t.nombre_tours} "
                    f"| Statut : {t.statut}"
                )

        print("-" * 30)
        print("[A] Créer un tournoi")
        print("[V] Voir les détails d’un tournoi")
        print("[R] Retour")

    def afficher_details_tournoi(self, tournoi: TournoiModel):
        """Affiche l'écran 'Détail d’un Tournoi'."""
        print("\n" + "=" * 5 + f" {tournoi.nom.upper()} " + "=" * 5)
        print(f"Lieu : {tournoi.lieu} | Date : {tournoi.date_debut} - {tournoi.date_fin}")
        print(f"Contrôle : {tournoi.controle_temps} | Tours prévus : {tournoi.nombre_tours}")

        print("-" * 40)
        if not tournoi.tours:
            print("Aucun tour n'a encore été généré.")
        else:
            for i, tour in enumerate(tournoi.tours):
                statut = "Terminé" if tour.date_heure_fin else "En cours"
                print(f"{i+1}. {tour.nom} - {statut}")

        print("-" * 40)
        print("[G] Générer un nouveau round")
        print("[S] Saisir résultats")
        print("[L] Liste des joueurs")
        print("[R] Retour")

    def obtenir_choix_tournoi(self) -> int | None:
        """Demande à l'utilisateur quel tournoi voir en détail."""
        try:
            choix = input("Numéro du tournoi à voir (ou R pour retour) : ").strip().upper()
            if choix == "R":
                return None
            return int(choix)
        except ValueError:
            print("Saisie invalide. Veuillez entrer un numéro.")
            return None

    def get_user_choice(self) -> str:
        """Demande et retourne le choix de l'utilisateur."""
        return input("Votre choix : ").strip().upper()

    # --- NOUVELLE MÉTHODE DE SAISIE ---

    def saisir_nouveau_tournoi(self) -> dict | None:
        """
        Collecte les informations nécessaires pour créer un nouveau tournoi.
        Retourne un dictionnaire de données ou None en cas d'annulation.
        """
        print("\n--- CRÉER UN NOUVEAU TOURNOI ---")

        # 1. Nom
        nom = input("Nom du tournoi : ").strip()
        if not nom:
            print("Annulé.")
            return None

        # 2. Lieu
        lieu = input("Lieu du tournoi : ").strip()

        # 3. Dates
        while True:
            try:
                date_debut_str = input("Date de début (AAAA-MM-JJ) : ").strip()
                date_fin_str = input("Date de fin (AAAA-MM-JJ) : ").strip()

                # Validation du format de date simple
                date_debut = date.fromisoformat(date_debut_str)
                date_fin = date.fromisoformat(date_fin_str)

                if date_debut > date_fin:
                    print("Erreur : La date de début ne peut pas être après la date de fin.")
                    continue
                break
            except ValueError:
                print("Erreur : Format de date invalide. Utilisez AAAA-MM-JJ.")

        # 4. Contrôle du Temps
        controle_temps_options = ["BLITZ", "RAPIDE", "COUP_RAPIDE"]
        while True:
            ct_str = input(
                f"Contrôle du temps ({'/'.join(controle_temps_options)}) : "
            ).strip().upper()
            if ct_str in controle_temps_options:
                controle_temps = ct_str
                break
            print(f"Erreur : Choix invalide. Veuillez choisir parmi {controle_temps_options}.")

        # 5. Nombre de tours
        while True:
            try:
                nb_tours_str = input("Nombre de tours (généralement 4) : ").strip()
                nombre_tours = int(nb_tours_str)
                if nombre_tours < 1:
                    raise ValueError
                break
            except ValueError:
                print("Erreur : Veuillez entrer un nombre de tours valide (chiffre positif).")

        # 6. Description
        description = input("Description générale (optionnel) : ").strip()

        return {
            "nom": nom,
            "lieu": lieu,
            "date_debut": date_debut_str,
            "date_fin": date_fin_str,
            "nombre_tours": nombre_tours,
            "controle_temps": controle_temps,
            "description": description,
        }
