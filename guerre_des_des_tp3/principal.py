"""
Point d'entrée du TP3.
"""

from random import shuffle

from afficheur import obtenir_couleurs_permises
from carte_autogeneree import CarteAutogeneree
from guerre_des_des import GuerreDesDes
from joueur_humain_console import JoueurHumainConsole
from joueur_ordinateur import JoueurOrdinateur

print("Bienvenue à la Guerre des dés!")


def demander_entier(nom_entier, entier_minimum=None, entier_maximum=None):
    """
    Cette fonction permet de demander à l'utilisateur un entier entre des bornes, possiblement
    absentes, avec validation de l'entrée.

    Args:
        nom_entier (str): Le mot à afficher
        entier_minimum (int, optional): La borne inférieure. Défaut: None (pas de borne inférieure)
        entier_maximum (int, optional): La borne supérieure. Défaut: None (pas de borne inférieure)

    Returns:
        int: L'entier entré par l'utilisateur
    """
    entree_invalide = True
    entier = None
    while entree_invalide:
        try:
            entier = int(input("Veuillez entrer {} : ".format(nom_entier)))
        except ValueError:
            pass
        if entier is not None:
            entier_trop_petit = entier_minimum is not None and entier < entier_minimum
            entier_trop_grand = entier_maximum is not None and entier > entier_maximum
            if entier_trop_petit:
                print("Entrée invalide: {} doit être un entier plus grand ou égal à {}. "
                      .format(nom_entier, entier_minimum))
            if entier_trop_grand:
                print("Entrée invalide: {} doit être un entier plus petit ou égal à {}. "
                      .format(nom_entier, entier_maximum))
            entree_invalide = entier_trop_petit or entier_trop_grand
    return entier


# On demande les dimensions de la carte à l'utilisateur, puis on crée la carte et l'affiche.
carte = None
while carte is None:
    hauteur = demander_entier("la hauteur", 3)
    largeur = demander_entier("la largeur", 3)
    n_trous = demander_entier("le nombre de cases vides", 0, hauteur * largeur)
    try:
        carte = CarteAutogeneree(largeur, hauteur, n_trous)
    except ValueError as value_error:
        print(value_error)
carte.afficher()

# On demande le nombre de joueurs humains et ordinateur à l'utilisateur et on leur associe des couleurs.
couleurs = obtenir_couleurs_permises()
shuffle(couleurs)
n_joueurs_max = len(couleurs)
n_joueurs_humains = demander_entier("le nombre de joueurs humains", 0, n_joueurs_max)
n_joueurs_ordinateurs = demander_entier("le nombre de joueurs ordinateurs", max(2 - n_joueurs_humains, 0),
                                        n_joueurs_max - n_joueurs_humains)
couleurs_joueurs_humains = couleurs[:n_joueurs_humains]
couleurs_joueurs_ordinateurs = couleurs[n_joueurs_humains:n_joueurs_humains + n_joueurs_ordinateurs]
joueurs = [JoueurHumainConsole(couleur) for couleur in couleurs_joueurs_humains] + \
          [JoueurOrdinateur(couleur) for couleur in couleurs_joueurs_ordinateurs]
shuffle(joueurs)

# On initialise la carte avec les joueurs et démarre une partie.
carte.diviser_territoires(joueurs)
gdd = GuerreDesDes(joueurs, carte)
gdd.afficher_joueurs()
input("Appuyez sur Entrée pour débuter...")
gdd.deroulement_global()
