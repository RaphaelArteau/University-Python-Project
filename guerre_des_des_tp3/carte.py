"""
Contient la classe Carte, qui gère l'ensemble des cases du jeu.
"""
from random import shuffle

import guerre_des_des_tp3.case
from guerre_des_des_tp3.afficheur import afficher


class Carte:
    def __init__(self, hauteur, largeur, cases):
        """
        Constructeur de la classe Case

        Args:
            hauteur (int): Le nombre de cases maximum de haut en bas
            largeur (int): Le nombre de cases maximum de gauche à droite
            cases (dict): L'ensemble des cases, avec leurs coordonnées comme clé.
        """

        self.hauteur = hauteur
        self.largeur = largeur
        self.cases = cases
        self.carte_prete = False

    def definir_voisins(self, cases):
        """
        Cette méthode attribue à chacune des cases des références vers ses voisins directs.

        Args:
            cases (dict): Les cases auxquelles attribuer les voisins
        """
        for case in cases.values():
            voisins_potentiels = [(case.coordonnees[0] + i, case.coordonnees[1] + j) for i, j in
                                  [(0, -1), (-1, 0), (1, 0), (0, 1)]]
            vrais_voisins = []
            for voisin_potentiel in voisins_potentiels:
                if voisin_potentiel in cases:
                    vrais_voisins.append(cases[voisin_potentiel])
            case.definir_voisins(vrais_voisins)

    def verifier_cases_connectees(self, cases):
        """
        Cette méthode retourne Vrai si toutes les cases sont connectées, c'est-à-dire
        qu'à partir de toute case il est possible de se rendre à toutes les autres. En d'autres
        mots, les trous ne séparent pas la carte en divers îlots.

        Args:
            cases (dict): Les cases dont on vérifie si elles sont connectées

        Returns:
            bool: True si les cases sont connectées, False sinon.
        """

        n_cases = len(cases)
        cases_vues = []
        frontiere = list(cases.values())[:1]

        while not len(frontiere) == 0:
            case = frontiere.pop()
            cases_vues.append(case)
            for voisin in case.voisins:
                if voisin not in cases_vues and voisin not in frontiere:
                    frontiere.append(voisin)

        return len(cases_vues) == n_cases

    def diviser_territoires(self, joueurs):
        """
        Cette méthode distribue la carte en un nombre égal de cases pour chaque joueur.
        Elle distribue également les dés initiaux.
        Cette méthode doit obligatoirement être exécutée entre le moment où les joueurs sont
        fixés et le début de la partie.

        Args:
            joueurs (list): La liste des joueurs.

        """
        coordonnees = list(self.cases.keys())
        shuffle(coordonnees)
        n_cases_par_joueur_base = len(coordonnees) // len(joueurs)
        n_cases_surplus = len(coordonnees) % len(joueurs)
        n_cases_par_joueur = []
        for j in range(len(joueurs)):
            n_cases_par_joueur.append(n_cases_par_joueur_base + int(j < n_cases_surplus))
        for i, joueur in enumerate(joueurs):
            for j in range(n_cases_par_joueur[i]):
                coor = coordonnees.pop()
                self.cases[coor].definir_appartenance(joueur)
            joueur.distribuer_surplus(self)
        self.carte_prete = True

    def taille_plus_grand_territoire(self, joueur):
        """
        Cette méthode retourne le nombre de cases faisant partie de la plus grande région
        connectée des cases d'un joueur spécifique.

        Args:
            joueur (Joueur): Le joueur dont on veut connaître la taille du plus grand territoire

        Returns:
            int: La taille du plus grand territoire du joueur

        """

        if not self.carte_prete:
            raise AssertionError("La carte doit d'abord être divisée en territoires. ")

        cases_joueur = self.obtenir_cases_joueur(joueur)
        cases_vues = set()
        max_territoire = 0
        for case_depart in cases_joueur.values():
            if case_depart not in cases_vues:
                territoire, territoire_non_vu = {case_depart}, {case_depart}
                while len(territoire_non_vu) > 0:
                    case_courante = territoire_non_vu.pop()
                    cases_vues.add(case_courante)
                    voisins_joueur = set(case_courante.voisins).intersection(set(cases_joueur.values()))
                    territoire.update(voisins_joueur)
                    territoire_non_vu = territoire.difference(cases_vues)
                max_territoire = max(max_territoire, len(territoire))
        return max_territoire

    def afficher(self):
        """
        Cette méthode affiche l'ensemble de la carte en chaîne de caractères.

        """

        afficher()
        afficher("x\\y |   ", end='')
        for x in list(range(self.largeur)):
            afficher('{:<5d}'.format(x), end='')
        afficher("\n" + "-" * 4 + "|-" + "-" * 5 * self.largeur)
        for i in range(self.hauteur):
            afficher("{:<3d} | ".format(i), end='')
            for j in range(self.largeur):
                if (i, j) in self.cases:
                    self.cases[(i, j)].afficher()
                else:
                    afficher("     ", end='')
            afficher()
        afficher()

    def obtenir_cases_joueur(self, joueur):
        """
        Cette méthode retourne les cases qui respectent ces critères:
            - Appartenir au joueur en argument

        Args:
            joueur (Joueur): Le joueur dont on veut obtenir les cases.

        Returns:
            dict: Le dictionnaire coordonnees:cases restreint à celle du joueur.

        """
        cases_joueur = {}
        for key in ([k for k, v in self.cases.items() if v.appartenance == joueur]):
            cases_joueur[key] = self.cases[key]
        return cases_joueur

    def obtenir_cases_ennemies(self, joueur):
        """
        Cette méthode retourne les cases qui respectent ces critères:
            - Ne pas appartenir au joueur en argument

        Args:
            joueur (Joueur): Le joueur dont on veut obtenir les cases qui ne lui appartiennent pas.

        Returns:
            dict: Le dictionnaire coordonnees:cases restreint à celle n'appartenant pas au joueur.

        """
        cases_ennemies = {}
        for key in ([k for k, v in self.cases.items() if v.appartenance != joueur]):
            cases_ennemies[key] = self.cases[key]
        return cases_ennemies

    def obtenir_cases_non_pleines(self, joueur):
        """
        Cette méthode retourne les cases qui respectent ces critères:
            - Appartenir au joueur en argument (Carte.obtenir_cases_joueur)
            - Ne pas être pleine (Case.est_pleine)

        Args:
            joueur (Joueur): Le joueur dont on veut obtenir les cases non pleines.

        Returns:
            dict: Le dictionnaire coordonnees:cases restreint à celle appartenant au joueur et non pleines.

        """
        cases_non_pleines = {}
        for key in ([k for k, v in self.obtenir_cases_joueur(joueur).items() if not v.est_pleine()]):
            cases_non_pleines[key] = self.cases[key]
        return cases_non_pleines

    def cases_disponibles_pour_defense(self, joueur, case_attaque):
        """
        Cette méthode retourne les cases qui respectent ces critères:
            - Ne pas appartenir au joueur en argument (Carte.obtenir_cases_ennemies)
            - Faire partie des voisins de la case qui attaque (Case.voisins)

        Args:
            joueur (Joueur): Le joueur possédant la case qui attaque.
            case_attaque(Case): La case qui attaque.

        Returns:
            dict: Le dictionnaire coordonnees:cases restreint à celles pouvant
                    se défendre de la case qui attaque.

        """
        cases_defense = {}
        for key in ([k for k, v in self.obtenir_cases_ennemies(joueur).items() if v in case_attaque.voisins]):
            cases_defense[key] = self.cases[key]
        return cases_defense


    def cases_disponibles_pour_attaque(self, joueur):
        """
        Cette méthode retourne les cases qui respectent ces critères:
            - Appartenir au joueur en argument (Carte.obtenir_cases_joueur)
            - Avoir au moins deux dés
            - Mener à une liste non vide de cases disponibles pour défense

        Args:
            joueur (Joueur): Le joueur dont on veut obtenir les cases pouvant attaquer.

        Returns:
            dict: Le dictionnaire coordonnees:cases restreint à celles appartenant
                    au joueur et pouvant attaquer.

        """
        cases_attaques = {}
        for k, v in self.obtenir_cases_joueur(joueur).items():
            for voisin in v.voisins:
                if voisin.appartenance != joueur and v.nombre_de_des() > 1:
                    cases_attaques[k] = self.obtenir_cases_joueur(joueur)[k]
        return cases_attaques

    def tout_deselectionner(self):
        """
        Cette méthode désélectionne toutes les cases (Case.deselectionner).
        """
        for key, value in self.cases.items():
            value.deselectionner()

