"""
Ce module comporte la classe JoueurHumainTk. Il s'agit d'une version du joueur
humain qui réagit aux clics dans l'interface (par opposition à entrer des coordonnées en console
au TP3).
"""

from guerre_des_des_tp3.joueur import Joueur


class JoueurHumainTk(Joueur):
    def __init__(self, couleur):
        """
        Constructeur de la classe JoueurHumainTk.

        Args:
            couleur (str): La couleur du joueur. Lui sert aussi de nom.
        """
        super().__init__(couleur, "Humain")

    def selectionner_attaquant(self, carte, coor):
        """
        Cette méthode permet de sélectionner l'attaquant.

        Args:
            carte (Carte): la carte du jeu.
            coor (tuple): les coordonnées de la case cliquée

        Returns:
            Case: la case aux coordonnées cliquées. None si elle n'est pas disponible.
        """
        cases_disponibles = carte.cases_disponibles_pour_attaque(self)
        if coor in cases_disponibles:
            case = cases_disponibles[coor]
            case.selectionner_pour_attaque()
            return case
        else:
            return None

    def selectionner_defenseur(self, carte, case_attaquante, coor):
        """
        Cette méthode permet de sélectionner le défenseur.

        Args:
            carte (Carte): la carte du jeu
            case_attaquante (Case): la case qui attaque
            coor (tuple): les coordonnées de la case cliquée

        Returns:
            Case: la case aux coordonnées cliquées. None si elle n'est pas disponible.
        """
        cases_disponibles = carte.cases_disponibles_pour_defense(self, case_attaquante)
        if coor in cases_disponibles:
            case = cases_disponibles[coor]
            case.selectionner_pour_defense()
            return case
        else:
            return None
