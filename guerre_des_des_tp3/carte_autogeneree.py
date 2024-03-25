"""
Contient la classe CarteAutogeneree, une sous-classe de Carte (la seule au TP3) générée
automatiquement selon les dimensions spécifiées
"""

from random import randint

from guerre_des_des_tp3.carte import Carte
from guerre_des_des_tp3.case import Case

# Cette constante contrôle le nombre de cartes générés aléatoirement avant d'abandonner
# car on ne trouve aucune configuration où tout le territoire est connecté.
N_ESSAIS_MAXIMUM = 100


class CarteAutogeneree(Carte):
    def __init__(self, hauteur, largeur, n_trous):
        """
        Constructeur de la classe CarteAutogeneree

        Args:
            hauteur (int): Le nombre de cases maximum de haut en bas
            largeur (int): Le nombre de cases maximum de gauche à droite
            n_trous (int): Le nombre de cases à enlever
        """

        super().__init__(hauteur, largeur, self.creer_carte(hauteur, largeur, n_trous))

    def creer_carte(self, hauteur, largeur, n_trous):
        """
        Cette méthode construit un dictionnaire de cases ayant hauteur*largeur - n_trous cases.
        Comme les trous sont placés aléatoirement, il se peut que la création mène à une
        carte non-connectée. Dans ce cas, on recommence jusqu'à ce qu'on obtienne une carte connectée.
        S'il est statistiquement trop improbable d'obtenir une carte connectée avec ces dimensions
        et ce nombre de trous, une exception est lancée.

        Args:
            hauteur (int): Le nombre de cases de haut en bas
            largeur (int): Le nombre de cases de gauche à droite
            n_trous (int): Le nombre de cases à enlever

        Returns:
            dict: Le dictionnaire de cases
        """
        
        cases_connectees = False
        n_essais = 0
        cases = {}
        while not cases_connectees:
            if n_essais > N_ESSAIS_MAXIMUM:
                raise ValueError("Trop de cases vides pour les dimensions")
            coordonnees = [(h, l) for h in range(hauteur) for l in range(largeur)]
            for _ in range(n_trous):
                del coordonnees[randint(0, len(coordonnees) - 1)]
            cases = {coor: Case(coor) for coor in coordonnees}
            self.definir_voisins(cases)
            cases_connectees = self.verifier_cases_connectees(cases)
            n_essais += 1
        return cases
