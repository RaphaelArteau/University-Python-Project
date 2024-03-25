"""
Contient la classe De, qui correspond à un dé. Le dé a 6 faces par défaut.
"""

from random import randint
from guerre_des_des_tp3.afficheur import afficher


class De:
    def __init__(self, nb_faces=6):
        """
        Constructeur de la classe De

        Args:
            nb_faces (int, optional): Le nombre de faces du dé (défaut: 6)
        """
        self.nb_faces = nb_faces

    def lancer(self):
        """
        Cette méthode retourne une valeur au hasard (random.randint) entre 1 et le
        nombre de faces, et affiche cette valeur (De.afficher_valeur).

        Returns:
            int: La valeur pigée.
        """
        return randint(1, self.nb_faces)
        # VOTRE CODE ICI

    def afficher_valeur(self, valeur):
        """
        Cette méthode affiche la valeur donnée en paramètre. Si le dé a 6 faces, on
        utilise un symbole spécial.

        Args:
            valeur: la valeur pigée à afficher
        """
        afficher(chr(9855 + valeur) if self.nb_faces == 6 else valeur, end=' ')