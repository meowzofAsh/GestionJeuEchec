from models.joueur_model import JoueurModel
from typing import List, Dict
from datetime import date


class JoueurView:
    """Gère l'interaction utilisateur pour la création et la gestion des joueurs."""

    def afficher_menu_joueurs(self, joueurs: List[JoueurModel]):
        """Affiche le menu des joueurs et la liste actuelle."""
        print("\n" + "=" * 15 + " JOUEURS " + "=" * 15)
        print(
            "ID | NOM | PRÉNOM | CLASSEMENT | SEXE | DATE DE NAISSANCE | POINTS"
        )
        print("-" * 75)

        if not joueurs:
            print("Aucun joueur enregistré.")
        else:
            for joueur in joueurs:
                dob_str = (
                    joueur.date_naissance.strftime("%Y-%m-%d")
                    if isinstance(joueur.date_naissance, date)
                    else str(joueur.date_naissance)
                )
                print(
                    f"{joueur.joueur_id:<2} | {joueur.nom_famille:<4} | "
                    f"{joueur.prenom:<6} | {joueur.classement:<10} | {joueur.sexe:<4} | "
                    f"{dob_str:<17} | {joueur.points_totaux}"
                )

        print("-" * 75)
        print("[A] Ajouter joueur | [M] Modifier classement | [T] Trier (afficher) | [R] Retour")

    def afficher_liste_joueurs_trie(self, joueurs: List[JoueurModel], titre: str):
        """Affiche une liste de joueurs triée (pour le rapport T)."""
        print(f"\n===== {titre.upper()} =====")
        self.afficher_menu_joueurs(joueurs)

    def saisir_nouveau_joueur(self) -> Dict | None:
        """
        Demande à l'utilisateur les données d'un nouveau joueur.
        Renvoie un dictionnaire prêt à être utilisé.
        """
        print("\n--- NOUVEAU JOUEUR ---")
        try:
            nom = input("Nom de famille : ").strip().upper()
            prenom = input("Prénom : ").strip().capitalize()
            dob_str = input("Date de naissance (AAAA-MM-JJ) : ").strip()
            sexe = input("Sexe (M/F) : ").strip().upper()
            classement = int(input("Classement (chiffre positif) : ").strip())

            if sexe not in ["M", "F"]:
                raise ValueError("Le sexe doit être 'M' ou 'F'.")

            date_obj = date.fromisoformat(dob_str)

            return {
                "nom_famille": nom,
                "prenom": prenom,
                "date_naissance": date_obj,
                "sexe": sexe,
                "classement": classement,
            }
        except ValueError as e:
            print(f"Erreur de format de saisie : {e}")
            return None

    def get_user_choice(self) -> str:
        """Demande et retourne le choix de l'utilisateur."""
        return input("Votre choix : ").strip().upper()
