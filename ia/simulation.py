"""
Ce fichier sert à effectuer une simulation afin de tester la performance de votre
intelligence artificielle programmée dans la classe JoueurOrdinateurAmeliore.

Par défaut, 100 parties à 3 sont jouées sur des
cartes auto-générées de taille 5x5 avec 8 trous.
À l'évaluation, 10 000 parties seront jouées, pour limiter la variance du pourcentage de victoires
"""

from random import shuffle

from guerre_des_des_tp3.afficheur import desactiver_affichage
from guerre_des_des_tp3.carte_autogeneree import CarteAutogeneree
from guerre_des_des_tp3.guerre_des_des import GuerreDesDes
from guerre_des_des_tp3.joueur_ordinateur import JoueurOrdinateur
from ia.joueur_ordinateur_ameliore import JoueurOrdinateurAmeliore
from ia.ai_raph import JoueurOrdinateurRaph
from ia.ai_jacob import JoueurOrdinateurAmelioreJacob

LARGEUR = 5
HAUTEUR = 5
N_TROUS = 8
N_SIMULATIONS = 100

desactiver_affichage()

VOTRE_IA = "Votre IA"
IA_PROF_1 = "IA1 du prof"
IA_PROF_2 = "IA2 du prof"

victoires = {
    VOTRE_IA: 0,
    IA_PROF_1: 0,
    IA_PROF_2: 0
}


def afficher_progression(ratio):
    """
    Cette fonction affiche une barre de progression correspondant à la fraction
    reçue en argument.

    Args:
        ratio (float): La fraction de progression, entre 0 et 1.
    """

    print("\rProgression: [{0:50s}] {1:.1f}%".format('#' * int(ratio * 50), ratio * 100),
          end="", flush=True)


for i in range(N_SIMULATIONS):
    afficher_progression(i / N_SIMULATIONS)
    joueurs = [JoueurOrdinateurAmeliore(VOTRE_IA), JoueurOrdinateur(IA_PROF_1), JoueurOrdinateur(IA_PROF_2)]
    shuffle(joueurs)
    carte = CarteAutogeneree(LARGEUR, HAUTEUR, N_TROUS)
    carte.diviser_territoires(joueurs)
    gdd = GuerreDesDes(joueurs, carte)
    gdd.deroulement_global()
    victoires[gdd.determiner_gagnant().couleur] += 1
afficher_progression(1)

pourcentage_victoire = 100 * victoires[VOTRE_IA] / N_SIMULATIONS
print("\nVotre IA a remporté {:.1f}% des parties!".format(pourcentage_victoire))

print("Cela vous donnera environ la note de {} / 25 pour cette section. ".format(
    max(min(2 * pourcentage_victoire - 55, 25), 0)
))
