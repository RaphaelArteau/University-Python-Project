## DICEWARS

DICEWARS est un jeu se jouant à plusieurs joueurs (humains ou ordinnateurs)
où chaque joueur tente d'obtenir le territoire le plus grand possible.
Chaque case contient un nombre de dés, et si la somme des dés d'une case attaquante
est strictement plus grande que celle de la somme des dés de la case défense,
l'attaquant prend pocession de la case. Un joueur gagne la partie lorsqu'il
possède l'ensemble des cases.


## Usage

Pour utiliser ce code, vous devez avoir une version 3.x de python et les packages suivants:
- pygame
Pour jouer à ce jeu, utilisez le module "principal.py"


## Liste des IAs

# IA Faible
IA codée par Louis Fortier-Dubois

# IA Moyenne
Choisit la case ayant la plus grande probabilité de réussir une attaque, et effectue l'attaque en question.

# IA Élevé
Essaie de construire le territoire le plus grand possible, en se connectant à ses "sous-territoires" existants.
Si aucune connection n'est possible, construit le plus long chemin possible (probabilité d'obtenir les cases défenses est élevée).
Attaque les cases les plus faibles aux endroits où la probabilité de réussite est la plus élevée.