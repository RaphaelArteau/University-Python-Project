"""
Contient le nécessaire pour afficher en console les différentes étapes du jeu.
L'affichage en console peut être aisément désactivé en appelant desactiver_affichage.
Contient également le nécessaire pour les couleurs des joueurs.

Attention: plusieurs des fonctionnalités offertes ici ne vous seront utiles qu'au TP4.
"""

from colorama import Fore, Style

# Variable qui contrôle la présence d'affichage en console
# Par défaut, l'affichage est activé.
affichage = True


def desactiver_affichage():
    """
    Cette fonction désactive l'affichage pour toute l'exécution du code.
    Utile au TP4 seulement.
    """
    global affichage
    affichage = False


# Dictionnaire qui associe les couleurs en français à leur équivalent dans la librairie colorama.
couleurs = {
    'rouge': Fore.RED,
    'bleu': Fore.BLUE,
    'jaune': Fore.YELLOW,
    'vert': Fore.GREEN,
    'magenta': Fore.MAGENTA,
    'cyan': Fore.CYAN
}

# Dictionnaire qui associe les couleurs en anglais à leur équivalent en français.
# Utile au TP4 seulement.
couleurs_interface = {
    'red': 'rouge',
    'blue': 'bleu',
    'yellow': 'jaune',
    'green': 'vert',
    'magenta': 'magenta',
    'cyan': 'cyan'
}


def obtenir_couleurs_permises():
    """
    Donne la liste des couleurs attribuables aux joueurs

    Returns:
        list: La liste des couleurs (str)

    """
    return list(couleurs.keys())


def coloriser_texte(texte, couleur):
    """
    Cette fonction donne un texte colorisé dans le format colorama

    Args:
        texte: Le texte à coloriser
        couleur: La couleur à attribuer (en français)

    Returns:
        str: Le texte colorisé, dans le format colorama

    """
    if couleur in couleurs:
        return "{couleur}{texte}{reset}" \
            .format(couleur=couleurs[couleur], texte=texte, reset=Style.RESET_ALL)
    else:
        return texte


def afficher(chaine='', couleur=None, end='\n'):
    """
    Cette fonction effectue un print colorisé, mais seulement si l'affichage est activé.

    Args:
        chaine: La chaîne à afficher
        couleur: La couleur à donner à la chaîne
        end: Caractère à ajouter en fin de ligne (comme pour print)

    """
    if affichage:
        print(coloriser_texte(chaine, couleur), end=end)


def demander(requete):
    """
    Cette fonction demande une valeur à l'utilisateur, mais seulement si l'affichage
    est activé. Cette fonction ne devrait pas être appelée si l'affichage est désactivé.

    Args:
        requete: La chaîne à afficher à l'utilisateur.

    Returns:
        str: L'entrée de l'utilisateur

    """
    if affichage:
        return input(requete)
    else:
        raise ValueError("On ne peut demander hors du mode affichage")
