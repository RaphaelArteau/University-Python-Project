"""
Ce module contient la classe CarteTeleversee. Celle-ci permet d'utiliser une carte de jeu
provenant d'un fichier texte. Ce fichier doit contenir des . là où il y aura une case, et des
espaces là où il y aura des trous. Évidemment, la carte doit être connectée (toutes les cases
sont accessibles).

Exemple valide:
.. ..
 ...
  .

Exemple invalide:
..
.  .
  ..

"""
from tkinter import messagebox

from guerre_des_des_tp3.carte import Carte
from guerre_des_des_tp3.case import Case

class CarteTeleversee(Carte):
    def __init__(self, nom_fichier):
        """
        Constructeur de la classe CarteTeleversee.

        Args:
            nom_fichier (str): Le nom du fichier contenant la carte sous forme de points.
        """
        cases = self.lire_fichier_carte(nom_fichier)
        if not cases:
            return None
        hauteur = 0
        largeur = 0
        for coor in cases.keys():
            hauteur = max(hauteur, coor[0] + 1)
            largeur = max(largeur, coor[1] + 1)
        super().__init__(hauteur, largeur, cases)

    def lire_fichier_carte(self, nom_fichier):
        """
        Cette méthode lit le fichier et convertit son contenu en cases.

        Args:
            nom_fichier (str): Le nom du fichier à lire

        Returns:
            dict: Le dictionnaire de cases, dont les clés sont les coordonnées.
        """
        #On essaie d'ouvrir le fichier, si inexistant, raise error
        try:
            fichier = open(nom_fichier, 'r')
        except:
            raise ValueError("Fichier introuvable")
        #On confirme que le fichier est txt, sinon raise error
        if not nom_fichier.endswith('.txt'):
            raise ValueError("Veuillez sectionner un fichier .txt")
        #longest = 0;
        #On crée des variables nécessaires pour la boucle
        #variable a retourner a la fin
        carte_a_retourner = {}
        #On commence à la ligne 0
        num_de_ligne = 0
        #Largeur de la carte finale
        largeur_de_la_carte = 0
        #Les seuls caracteres qui sont permis
        caracteres_permis = ['.',' ',"\n"]
        #On lit chaque ligne de la carte
        for ligne in fichier.readlines():
            #Le premier caractere est dans la colonne 0
            num_de_colonne = 0
            #On lit chaque colonne de la ligne
            for caractere in ligne:
                #Si le caractere n'est pas dans la liste, on raise une erreur
                if caractere not in caracteres_permis:
                    raise ValueError("Fichier contient un charactere invalide")
                #Si le caractere est un point, on crée une case
                if caractere == ".":
                    #Les coordonnées de la case sera le numero de ligne et de colonne
                    coor = (num_de_ligne, num_de_colonne)
                    carte_a_retourner[coor] = Case(coor)
                #On passe a la prochaine colonne
                num_de_colonne += 1
                #Si la colonne est plus grade que la largeur, on met la largeur selon la colonne
                if num_de_colonne > largeur_de_la_carte:
                    largeur_de_la_carte = num_de_colonne
            #On passe a la prochaine ligne
            num_de_ligne += 1
        #On crée une carte test pour confirmer que les cases se connectent bien, sinon raise error
        CarteTest = Carte(num_de_ligne, largeur_de_la_carte, carte_a_retourner)
        CarteTest.definir_voisins(carte_a_retourner)
        if not CarteTest.verifier_cases_connectees(carte_a_retourner):
            raise ValueError("La carte contient des cases non connectées")
        return carte_a_retourner

