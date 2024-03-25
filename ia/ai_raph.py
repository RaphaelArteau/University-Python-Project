from guerre_des_des_tp3.joueur_ordinateur import JoueurOrdinateur

class JoueurOrdinateurRaph(JoueurOrdinateur):

    def __init__(self, couleur, carte):
        super().__init__(couleur)
        #self.strategie_set = False
        self.carte = carte
        #self.max_move = self.carte.hauteur // 2
        self.path_to_complete = []

    def mine(self, case):
        return case.appartenance == self

    def trouver_les_territoires(self):
        case_par_joueur = {}
        des_par_joueur = {}
        cases = self.carte.cases
        for coordonnees in cases:
            case = cases[coordonnees]
            joueur = case.appartenance
            nb_des = case.nombre_de_des()
            if joueur not in case_par_joueur:
                case_par_joueur[joueur] = {}
                des_par_joueur[joueur] = 0
            des_par_joueur[joueur] = des_par_joueur[joueur] + nb_des
            case_par_joueur[joueur][coordonnees] = case
        self.cur_nb_des = des_par_joueur[self]
        self.mes_cases = case_par_joueur[self]
        cases = self.mes_cases
        voisins_par_case = {}
        for coor, case in cases.items():
            voisins_par_case[coor] = []
            for voisin in case.voisins:
                if self.mine(voisin):
                    voisins_par_case[coor].append(voisin.coordonnees)
        index = 0
        while index < len(voisins_par_case.keys()):
            coor = list(voisins_par_case.keys())[index]
            voisins = voisins_par_case[coor]
            index2 = 0
            while index2 < len(voisins):
                voisin = voisins[index2]
                if voisin in voisins_par_case.keys():
                    voisins_par_case[coor] = voisins_par_case[coor] + voisins_par_case[voisin]
                    voisins_par_case.pop(voisin)
                if coor in voisins_par_case[coor]:
                    voisins_par_case[coor].remove(coor)
                voisins = voisins_par_case[coor]
                index2 += 1
            index += 1
        territories = []
        for case, voisins in voisins_par_case.items():
            territories.append([case]+list(set(voisins)))
        self.mes_territoires = territories
        self.territoires_de_connection = []
        for territoire in self.mes_territoires:
            cases_de_connections = []
            for coor in territoire:
                case = self.carte.cases[coor]
                """
                if case.appartenance == self:
                    continue
                """
                for voisin in case.voisins:
                    n_coor = voisin.coordonnees
                    if n_coor not in cases_de_connections and voisin.appartenance != self:
                        cases_de_connections.append(n_coor)
            self.territoires_de_connection.append(cases_de_connections)
        return self.mes_territoires

    def analyser_la_situation(self, cases_disponibles):
        self.paths = []
        for coor, case in cases_disponibles.items():
            self.trouver_tous_les_chemins(case)
        self.possibles_paths = {}
        for path in self.paths:
            base = path.pop(0)
            case = cases_disponibles[base]
            if base not in self.possibles_paths:
                self.possibles_paths[base] = []
            if len(path) > 0:
                nb_des = case.nombre_de_des()
                cases = 0
                chances_de_gagner = []
                biggest_dif = 0
                des_enveles = 0
                for voisin in self.carte.cases[base].voisins:
                    if voisin.appartenance != self and voisin.coordonnees not in path:
                        dif = voisin.nombre_de_des() - 1
                        if dif > biggest_dif:
                            biggest_dif = dif
                for p in path:
                    if p == path[-1]:
                        compare = nb_des
                    else:
                        compare = 1

                    n_case = self.carte.cases[p]

                    for voisin in n_case.voisins:
                        if voisin.appartenance != self and voisin.coordonnees not in path:
                            dif = voisin.nombre_de_des() - compare
                            if dif > biggest_dif:
                                biggest_dif = dif

                    nb_des_def = n_case.nombre_de_des()
                    des_enveles = des_enveles + nb_des_def
                    chances_de_gagner.append(self.chance_de_gagner(nb_des_def, nb_des))
                    nb_des -= 1
                    cases += 1
                self.possibles_paths[base].append({
                    "case_dorigine": base,
                    "path": path,
                    "chances": chances_de_gagner,
                    "des_qui_sera_enlever": des_enveles,
                    "chances_globales": sum(chances_de_gagner) / len(chances_de_gagner),
                    "cases": cases,
                    "biggest_dif" : biggest_dif
                })

    def strategie_selection_attaquant(self, cases_disponibles):
        """
        if input("Continue ?") == "n":
            exit()
        """

        if len(self.path_to_complete) > 0:
            if self.path_to_complete[0] in cases_disponibles and len(self.path_to_complete) != 1:
                #print("Finishing queue")
                case = self.path_to_complete[0]
                self.path_to_complete.pop(0)
                return case
            else:
                self.path_to_complete = []

        self.analyser_la_situation(cases_disponibles)
        self.trouver_les_territoires()

        #1. On se demande si on peut se connecter à d'autres territoires
        chances_de_connections = []
        for case, paths in self.possibles_paths.items():
            for index in range(0, len(self.mes_territoires)):
                if case in self.mes_territoires[index]:
                    case_dans_territoire = index
            for chemin in paths:
                case_final = chemin["path"][-1]
                for index in range(0, len(self.mes_territoires)):
                    if index != case_dans_territoire:
                        if case_final in self.territoires_de_connection[index]:
                            chances_de_connections.append(chemin)
        meilleure_chance = {
            "chances_globales": 0
        }
        if len(chances_de_connections) > 0:
            for connection in chances_de_connections:
                """
                if self.max_move < 5:
                    if connection["biggest_dif"] >= self.max_move:
                        continue
                """
                if connection["chances_globales"] > meilleure_chance["chances_globales"]:
                    meilleure_chance = connection

        if meilleure_chance["chances_globales"] > 0.5:
            #print("Path 1")
            self.path_to_complete = meilleure_chance["path"]
            return meilleure_chance["case_dorigine"]

        """
        if self.carte.hauteur < 15:
            tot_des_enlever = {}
            for coor, paths in self.possibles_paths.items():
                for path in paths:
                    try:
                        tot_des_enlever[path["des_qui_sera_enlever"]]
                    except:
                        tot_des_enlever[path["des_qui_sera_enlever"]] = []
                    tot_des_enlever[path["des_qui_sera_enlever"]].append(path)
            keys = tot_des_enlever.keys()
            for k in reversed(keys):
                for chemin in tot_des_enlever[k]:
                    if chemin["chances_globales"] > 0.6:
                        self.path_to_complete = chemin["path"]
                        return chemin["case_dorigine"]
            #exit()
        """

        longueur_par_chance = {
            "longueur_par_chance" : 0
        }
        for case, paths in self.possibles_paths.items():
            for chemin in paths:
                """
                if chemin["cases"] > 1:
                    continue
                """
                """
                if self.max_move < 5:
                    if chemin["biggest_dif"] >= self.max_move:
                        continue
                """
                tmp = chemin["chances_globales"] * chemin["cases"]
                chemin["longueur_par_chance"] = tmp
                if chemin["longueur_par_chance"] > longueur_par_chance["longueur_par_chance"]:
                    longueur_par_chance = chemin
        if longueur_par_chance["longueur_par_chance"] > 0:
            if longueur_par_chance["chances_globales"] > 0.6:
                #print("Path 2")
                self.path_to_complete = longueur_par_chance["path"]
                return longueur_par_chance["case_dorigine"]

        for coor, case in cases_disponibles.items():
            nb_des = case.nombre_de_des()
            for voisin in case.voisins:
                if voisin.appartenance == self:
                    continue
                nb_des_voisin = voisin.nombre_de_des()
                chances = self.chance_de_gagner(nb_des_voisin,nb_des)
                if chances > 0.5:
                    #print("Path 3")
                    self.path_to_complete = [voisin.coordonnees]
                    return coor

        return None

    def strategie_selection_defenseur(self, cases_disponibles, case_attaquant):
        if len(self.path_to_complete) > 0:
            case = self.path_to_complete[0]
            return case
        return None

    def __recursive_function__(self, case, des_dispo, array = []):
        voisins_visitables = []
        n_array = array.copy()
        n_array.append(case.coordonnees)
        for voisin in case.voisins:
            if voisin.appartenance != self and voisin.nombre_de_des() < des_dispo and voisin.coordonnees not in n_array:
                voisins_visitables.append(voisin)
        #if len(voisins_visitables) == 0:
        self.paths.append(n_array)
        for n_case in voisins_visitables:
            self.__recursive_function__(n_case,des_dispo-1,n_array)

    def trouver_tous_les_chemins(self, case):
        des_dispo = case.nombre_de_des()
        self.__recursive_function__(case, des_dispo, [])

    def chance_de_gagner(self, defandant, attanquant, nb_face=6):
        tot = 0
        gagne = 0
        for i in range(defandant, defandant * nb_face + 1):
            for x in range(attanquant, attanquant * nb_face + 1):
                tot += 1
                if x > i:
                    gagne += 1
        return gagne / tot
