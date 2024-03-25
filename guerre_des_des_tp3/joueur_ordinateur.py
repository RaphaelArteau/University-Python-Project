"""
Contient la classe JoueurOrdinateur, qui hérite de Joueur. Cette classe implémente une intelligence
artificielle pour choisir l'attaquant et le défenseur.

La stratégie de l'intelligence artificielle est la suivante:
À chaque attaque elle a une chance sur 5 d'arrêter son tour
Si elle attaque:
    Elle sélectionne l'attaquant ayant le plus de dés
    Si des voisins ont 1 ou 2 dés de moins, elle attaque le plus fort d'entre eux
    Sinon, si un voisin a autant de dés qu'elle, elle l'attaque
    Sinon, si un voisin a au moins 3 dés de moins qu'elle, elle attaque le plus fort d'entre eux
    Sinon, elle a une chance sur deux d'attaquer le voisin le plus faible parmi ceux qui sont
        plus forts qu'elle, sinon elle retourne à la phase de choix de l'attaquant
Dans tous les cas, les égalités sont brisées arbitrairement.
"""
import operator

from guerre_des_des_tp3.joueur import Joueur
from random import randint


class JoueurOrdinateur(Joueur):
    def __init__(self, couleur):
        """
        Constructeur de la classe JoueurOrdinateur
        Args:
            couleur: la couleur du joueur
        """
        super().__init__(couleur, "joueur ordinateur")

    def filtrer_nb_des(self, cases, valeurs_acceptees):
        """
        Cette méthode retourne les cases dont le nombre de dés (Case.nombre_de_des)
        fait partie des valeurs de nombres de dés acceptés.

        Args:
            cases (dict): Les cases du jeu
            valeurs_acceptees (list): La liste des nombres de dés à conserver

        Returns:
            dict: Les cases du jeu dont le nombre de dés fait partie des valeurs acceptées

        """
        cases_acceptees = {}
        for key in ([k for k, v in cases.items() if v.nombre_de_des() in valeurs_acceptees]):
            cases_acceptees[key] = cases[key]
        return cases_acceptees

        # VOTRE CODE ICI (A VERIFIER)

    def trouver_nb_des_optimal(self, cases, minimum=False):
        """
        Cette méthode trouve la case ayant le maximum OU le minimum de dés.
        Si l'option minimum n'est pas cochée, on trouve la case ayant le plus grand nombre de dés.
        Si l'option minimum est cochée, on trouve la case ayant le plus petit nombre de dés.
        Vous pouvez utiliser des sous-méthodes si cela vous facilite le travail.

        Dans le cas d'une égalité (e.g. plusieurs cases ont le maximum de dés), vous pouvez
        sélectionner n'importe laquelle de ces cases (au hasard, toujours la dernière visitée par
        votre algorithme, ...).

        Args:
            cases (dict): Les cases parmi lesquelles chercher
            minimum (bool, optionnel): Si True, trouver le minimum, si False, trouver le maximum.
                Défaut: False

        Returns:
            Case: la case sélectionnée
        """
        nb_optimal_case = {}

        for k, v in cases.items():
            nb_optimal_case[k] = cases[k].nombre_de_des()
        if not minimum:
            return max(nb_optimal_case, key=nb_optimal_case.get, default=None)
        else:
            return min(nb_optimal_case, key=nb_optimal_case.get, default=None)

    def strategie_selection_attaquant(self, cases_disponibles):
        """
        Cette méthode implémente l'intelligence artificielle (IA) permettant de sélectionner
        un attaquant.

        Args:
            cases_disponibles (dict): Les cases disponibles pour attaque

        Returns:
            Case: La case sélectionnée par l'IA. None si elle arrête son tour.
        """
        # L'IA a une chance sur 5 d'arrêter son tour
        if randint(1, 5) == 1:
            return None

        # L'IA sélectionne l'attaquant ayant le plus de dés
        return self.trouver_nb_des_optimal(cases_disponibles)

    def strategie_selection_defenseur(self, cases_disponibles, case_attaquante):
        """
        Cette méthode implémente l'intelligence artificielle (IA) permettant de sélectionner
        un défenseur.

        Args:
            cases_disponibles (dict): Les cases disponibles pour attaque
            case_attaquante (Case): La case qui attaque

        Returns:
            Case: La case sélectionnée par l'IA. None si elle retourne à la phase de
            sélection de l'attaquant.
        """

        # Si des voisins ont 1 ou 2 dés de moins, l'IA attaque le plus fort d'entre eux
        case_defense = self.trouver_nb_des_optimal(
            self.filtrer_nb_des(cases_disponibles,
                                [case_attaquante.nombre_de_des() - 1, case_attaquante.nombre_de_des() - 2])
        )
        if case_defense is not None:
            return case_defense

        # Sinon, si un voisin a autant de dés que l'IA, elle l'attaque
        case_defense = self.trouver_nb_des_optimal(
            self.filtrer_nb_des(cases_disponibles, [case_attaquante.nombre_de_des()])
        )
        if case_defense is not None:
            return case_defense

        # Sinon, si un voisin a au moins 3 dés de moins que l'IA, elle attaque le plus fort d'entre eux
        case_defense = self.trouver_nb_des_optimal(
            self.filtrer_nb_des(cases_disponibles,
                                [case_attaquante.nombre_de_des() - i for i in
                                 range(3, case_attaquante.nombre_de_des())])
        )
        if case_defense is not None:
            return case_defense

        # Sinon, l'IA attaque le voisin le plus faible parmi ceux qui sont plus forts qu'elle
        if randint(1, 2) == 1:
            return self.trouver_nb_des_optimal(cases_disponibles, minimum=True)
        else:
            return None
