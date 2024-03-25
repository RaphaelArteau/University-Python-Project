"""
Ce module contient la classe CanvasCarte, qui permet de dessiner l'ensemble de la carte
et de gérer les clics.
"""
from tkinter import Canvas, ALL, Tk, messagebox
from pygame import mixer
from PIL import ImageTk, Image
from guerre_des_des_tp3.carte import Carte
from interface.joueur_humain_tk import *
from interface.parametres import __parametres__
from interface.probabilites import probabilite_attaque_reussie
from interface.fenetre_temporaire import JacobWindow



class CanvasCarte(Canvas):
    def __init__(self, parent, carte, resolution_hauteur):
        """
        Constructeur de la classe CanvasCarte. Attribue les dimensions en pixels
        en fonction des dimensions de la carte, dessine la carte dans l'interface
        et associe le clic de souris à la méthode selectionner_case.

        Args:
            parent (Tk): Le widget TKinter dans lequel le canvas s'intègre.
            carte (Carte): La carte de la guerre des dés à afficher.
        """
        self.textes_dans_cases = {}
        self.carte = carte
        self.parent = parent
        ratio = self.carte.hauteur / self.carte.largeur
        DIMENSION_BASE = resolution_hauteur * 0.65

        self.hauteur_canvas = DIMENSION_BASE
        self.largeur_canvas = int(DIMENSION_BASE//ratio)
        self.attaque_speciale_en_cours = None

        super().__init__(parent, width=self.largeur_canvas, height=self.hauteur_canvas,
                         borderwidth=0, highlightthickness=0)
        self.bind("<Button-1>", self.selectionner_case)
        self.case_selectionnee = None
        self.count = 0

        #self.hauteur_case = self.hauteur_canvas // self.carte.hauteur
        #self.largeur_case = self.largeur_canvas // self.carte.largeur
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        if self.carte.largeur > 50:
            num = 180
        else:
            num = 120
        min_largeur_case = (screen_width - num)/self.carte.largeur
        min_hauteur_case = (screen_height - 375)/self.carte.hauteur
        self.taille = min(min_largeur_case, min_hauteur_case)
        self.configure(width=self.taille * self.carte.largeur, height=self.taille * self.carte.hauteur)

        if self.taille < 15:
            raise ValueError("L'écran est trop petit pour cette carte")
        if self.taille < 25:
            __parametres__.setSession("zoom_recursif", False)
        self.largeur_case = self.hauteur_case = self.taille

        self.canvas_centre()
        
    def canvas_centre(self):
        """
        Position de la fenêtre en haut au centre de l'écran
        """
        self.update()
        screen_width = self.winfo_screenwidth()
        x_cordinate = int((screen_width / 2) - (self.winfo_reqwidth() / 2))
        self.master.geometry(f'+{int(x_cordinate)}+{0}')

    def pixel_vers_coordonnees(self, x, y):
        """
        Cette méthode convertit la position d'un clic en coordonnées de la carte.

        Args:
            x: La position du clic, en x (de haut en bas)
            y: La position du clic, en y (de gauche à droite)

        Returns:
            tuple: Les coordonnées de la case cliquée.
        """
        try:
            self.case_selectionnee = self.carte.cases[x // self.hauteur_case, y // self.largeur_case]
            return x // self.hauteur_case, y // self.largeur_case
        except:
            pass

    def coordonnees_vers_pixels(self, x, y):
        """
        Cette méthode des coordonnées de la carte en position en pixels

        Args:
            x: La coordonnée en x
            y: La coordonnée en y

        Returns:
            tuple: La position en pixels.
        """
        return x * self.hauteur_case, y * self.largeur_case

    def probabilite(self):
        try:
            case_selectionnee = self.carte.cases[self.derniere_case_click]
        except:
            return
        joueur = self.parent.joueur_actuel
        if case_selectionnee.appartenance != joueur or case_selectionnee.nombre_de_des() == 1:
            return
        nb_des_attaque = case_selectionnee.nombre_de_des()
        dico = {}
        for voisin in case_selectionnee.voisins:
            if voisin.appartenance != joueur:
                nb_des_def = voisin.nombre_de_des()
                dico[voisin.coordonnees] = probabilite_attaque_reussie(nb_des_attaque, nb_des_def)
        JacobWindow(self.parent, dico)

    def selectionner_case(self, event):
        """
        Cette méthode prend en argument un clic de souris sur le canvas, et actionne
        la fonction définie comme devant faire suite au clic (self.suite_clic), dont
        l'argument est en coordonnées plutôt qu'en pixels.

        Args:
            event (tkinter.Event): L'événement correspondant au clic

        """
        x, y = event.y, event.x  # nos coordonnées sont transposées par rapport aux pixels
        self.derniere_case_click = coor = self.pixel_vers_coordonnees(x, y)
        if self.attaque_speciale_en_cours == None and __parametres__.get("aide_prob"):
            self.probabilite()
        if self.attaque_speciale_en_cours != None:
            if self.attaque_speciale_en_cours == "explotion":
                joueur = self.joueur_action_speciale
                case = self.carte.cases[coor]
                if case.appartenance == joueur:
                    messagebox.showerror("Erreur","Vous ne pouvez faire exploser une de vos cases.")
                else:
                    coor_principal = coor
                    voisins_par_case = {}
                    for coor, case in self.carte.cases.items():
                        voisins_par_case[coor] = []
                        for voisin in case.voisins:
                            voisins_par_case[coor].append(voisin.coordonnees)
                    index = 0
                    del voisins_par_case[coor_principal]
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
                        territories.append([case] + list(set(voisins)))
                    if len(territories) > 1:
                        messagebox.showerror("Erreur", "Cette case ne peut être supprimée")
                    else:
                        confirm = messagebox.askokcancel("Confirmation", "Voulez-vous vraiment supprimer cette case ?")
                        if confirm :
                            del self.carte.cases[coor_principal]
                            def rien():
                                pass
                            self.parent.redessiner(rien)
                            self.attaque_speciale_callback()
                return
            if self.attaque_speciale_en_cours == "voler_case":
                joueur = self.joueur_action_speciale
                case = self.carte.cases[coor]
                if case.appartenance == joueur:
                    messagebox.showerror("Erreur","Cette case vous appartient déjà")
                else:
                    confirm = messagebox.askokcancel("Confirmation", "Voulez-vous vraiment voler cette case ?")
                    if confirm:
                        self.carte.cases[coor].appartenance = joueur
                        def rien():
                            pass
                        self.parent.redessiner(rien)
                        self.attaque_speciale_callback()
                return
            if self.attaque_speciale_en_cours == "voler_des":
                joueur = self.joueur_action_speciale
                case = self.carte.cases[coor]
                if case.appartenance == joueur:
                    messagebox.showerror("Erreur", "Ces dés vous appartiennent déjà")
                else:
                    confirm = messagebox.askokcancel("Confirmation",
                                                     "Voulez-vous vraiment voler les dés de cette case ?")
                    if confirm:
                        des_a_garder = case.des
                        self.carte.cases[coor].des = [des_a_garder[0]]
                        joueur.ajouter_n_des(des_a_garder[1:])
                        def rien():
                            pass
                        self.parent.redessiner(rien)
                        self.attaque_speciale_callback()
                return
        if self.suite_clic is not None:
            self.suite_clic(coor)
            
    def musique_jeu(self, fichier, repetition):
        if repetition < 1:
            mixer.find_channel().play(mixer.Sound(fichier))

    def dessiner_canvas(self, joueur):
        """
        Cette méthode dessine la carte.
        """
        path = "tank.png"
        tank = Image.open(path)
        largeur, hauteur = tank.size
        largeur_tank = int((largeur / hauteur) * self.taille/1.6)
        hauteur_tank = int((hauteur / largeur) * self.taille/1.6)
        tank = tank.resize((largeur_tank, hauteur_tank))
        self.photo_tank = ImageTk.PhotoImage(tank)

        path = "explosion2.png"
        explosion = Image.open(path)
        largeur, hauteur = explosion.size
        largeur_explosion = int((largeur / hauteur) * self.taille//1.6)
        hauteur_explosion = int((hauteur / largeur) * self.taille//1.6)
        explosion = explosion.resize((largeur_explosion, hauteur_explosion))
        self.photo_explosion = ImageTk.PhotoImage(explosion)
        
        self.delete(ALL)
        for (x, y), case in self.carte.cases.items():
            self.font_size = font_size = 20
            outline, width = 'black', 1
                
            haut, gauche = self.coordonnees_vers_pixels(x, y)
            bas, droite = self.coordonnees_vers_pixels(x + 1, y + 1)

            case_dessin = self.create_rectangle(gauche, haut, droite-width, bas-width, fill=case.appartenance.couleur,
                                               outline='black', width=width)

            case_texte = self.create_text((gauche + droite) // 2, (haut + bas) // 2, fill='black',
                             font="Times {} bold".format(font_size), text=len(case.des))


            # Bind de la fonction recursive a la case pour le zoom récursive
            self.tag_bind(case_dessin, "<Enter>", lambda event, arg1=(x, y): self.zoom_recursif(event, arg1))
            self.textes_dans_cases[(x,y)] = case_texte

            if isinstance(joueur, JoueurHumainTk) and self.case_selectionnee is not None:
                cases_defenses = self.carte.cases_disponibles_pour_defense(joueur, self.case_selectionnee)
            else:
                cases_defenses = None

            if all(case.mode == 'attente' for case in self.carte.cases.values()) and \
                    case in list(self.carte.cases_disponibles_pour_attaque(joueur).values()):
                self.count = 0
                self.cases_clignotent(joueur.couleur, case_dessin, 0)

            if case.mode == 'attaque':
                if __parametres__.get("war_mode"):
                    self.create_image((gauche + droite) // 2, (haut + bas) // 2, image=self.photo_tank)
                else:
                    self.itemconfig(case_texte, text='⚔', font="Times {} bold".format(int((self.hauteur_canvas //
                                                                                           self.carte.hauteur)//2.4)))

            if cases_defenses is not None and case in list(cases_defenses.values()) \
                    and isinstance(joueur, JoueurHumainTk) and \
                    any(case_attaque.mode == 'attaque' for case_attaque in self.carte.cases.values()):
                self.cases_clignotent(case.appartenance.couleur, case_dessin, 0)

            if case.mode == 'defense':
                #print(self.selectionner_case)
                if __parametres__.get("war_mode"):
                    if self.count == 0:
                        self.musique_jeu('tankshot.mp3', self.count)
                        self.after(500)
                        self.count += 1
                    else:
                        self.create_image((gauche + droite) // 2, (haut + bas) // 2, image=self.photo_explosion)
                        self.after(500)
                        self.musique_jeu('explosion.mp3', self.count - 1)
                else:
                    if case.mode == 'defense':
                        self.itemconfig(case_texte, text='🛡', font="Times {} bold"
                                        .format(int((self.hauteur_canvas // self.carte.hauteur)//2)))

    def zoom_recursif(self, event, coor, taille_texte=False,premiereTournee=False):
        if coor not in self.carte.cases:
            return
        if not __parametres__.get("zoom_recursif"):
            return False
        if not taille_texte:
            taille_texte = self.font_size * 2
        if not premiereTournee:
            for case in self.textes_dans_cases.values():
                self.itemconfig(case,font="Times {} bold".format(self.font_size))
            self.cases_deja_affectee = []
        self.itemconfig(self.textes_dans_cases[coor], font="Times {} bold".format(taille_texte))
        self.cases_deja_affectee.append(coor)
        taille_texte -= 8
        if taille_texte > self.font_size:
            voisins = self.carte.cases[coor].voisins
            for voisin in voisins:
                coor2 = voisin.coordonnees
                if coor2 not in self.cases_deja_affectee:
                    self.zoom_recursif(None, coor2, taille_texte, True)


    def cases_clignotent(self, couleur, rectangle, index):
        couleurs = (couleur, couleur + '3')
        self.itemconfig(rectangle, fill=couleurs[index])
        self.after(500, self.cases_clignotent, couleur, rectangle, 1 - index)

    def permettre_clics(self, suite_clic):
        """
        Cette méthode associe une fonction à exécuter à ce qui doit arriver suite
        à un clic.
        """
        self.suite_clic = suite_clic
