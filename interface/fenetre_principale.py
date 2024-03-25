"""
Module contenant la classe FenetrePrincipale et ses classes utilitaires FrameAttaque
et FrameJoueurActif. Cette fenêtre permet de jouer au jeu.
"""
import tkinter
from random import choice
from tkinter import Tk, Frame, Button, Label, messagebox, Checkbutton, GROOVE, Canvas, RIGHT, LEFT, Toplevel
from PIL import ImageTk, Image
from PIL.ImageTk import PhotoImage

from guerre_des_des_tp3.afficheur import desactiver_affichage, couleurs_interface
from guerre_des_des_tp3.guerre_des_des import GuerreDesDes
from interface.canvas_carte import CanvasCarte
from interface.elements_tkinter_perso import ButtonCoinsRonds
from interface.fenetre_introduction import FenetreIntroduction
from guerre_des_des_tp3.joueur_ordinateur import JoueurOrdinateur
from interface.parametres import __parametres__, BG_COLOR, FG_COLOR, __nom_pour_le_fun__
from interface.energy_bar import EnergyBar

# Le temps entre chaque décision de l'ordinateur et pour chaque bataille, en millisecondes.
from interface.joueur_humain_tk import JoueurHumainTk
from interface.parametres import __parametres__

# Musique
from pygame import mixer
from interface.audio import FenetreAudio
liste_musics = ["While True.mp3", "We Are The Champions.mp3", "I Will Survive.mp3"]

TEMPS_ATTENTE = 100


class FrameAttaque(Frame):
    def __init__(self, parent):
        """
        Constructeur de la classe FrameAttaque. Affiche les informations relatives
        aux attaques.

        Args:
            parent (Tk): La fenêtre dans laquelle ce frame s'insert.
        """
        super().__init__(parent)
        self.label_joueur_attaque = Label(self, text="", font=("Winden", 16))
        self.label_force_attaque = Label(self, text="", font=("Winden", 16))
        self.label_joueur_defense = Label(self, text="", font=("Winden", 16))
        self.label_force_defense = Label(self, text="", font=("Winden", 16))

        self.label_joueur_attaque.grid(row=0, column=0)
        self.label_force_attaque.grid(row=0, column=1)
        self.label_joueur_defense.grid(row=1, column=0)
        self.label_force_defense.grid(row=1, column=1, pady=3)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def populer(self, joueur_attaque, force_attaque, joueur_defense, force_defense):
        """
        Cette méthode affiche les informations d'une attaque.

        Args:
            joueur_attaque (Joueur): Le joueur qui attaque
            force_attaque (int): La somme des dés de l'attaquant
            joueur_defense (Joueur): Le joueur qui se défend
            force_defense (int): La somme des dés du défenseur
        """
        self.label_joueur_attaque['fg'] = joueur_attaque.couleur
        self.label_joueur_attaque['text'] = "{} \tAttaquant: ".format('⚔')

        self.label_force_attaque['fg'] = joueur_attaque.couleur
        self.label_force_attaque['text'] = '{} \t🎲'.format(force_attaque)

        self.label_joueur_defense['fg'] = joueur_defense.couleur
        self.label_joueur_defense['text'] = "{:>2s} \tDéfenseur: ".format('🛡')

        self.label_force_defense['fg'] = joueur_defense.couleur
        self.label_force_defense['text'] = '{} \t🎲'.format(force_defense)

    def vider(self):
        """
        Cette méthode enlève l'affichage des attaques.
        """
        self.label_joueur_attaque['text'] = ""
        self.label_force_attaque['text'] = ""
        self.label_joueur_defense['text'] = ""
        self.label_force_defense['text'] = ""

class FrameMessage(Frame):
    def __init__(self, parent):
        """
        Constructeur de la classe FrameMessage. Affiche les messages des attaques réussies ou non.

        Args:
            parent (Tk): La fenêtre dans laquelle ce frame s'insert.
        """

        super().__init__(parent)
        self.label_resultat = Label(self, text="", font=("Arial", 16), width=55, height=2,
                                    bg="white smoke", padx=5, pady=5, wraplength=600, relief="sunken")

        self.label_resultat.grid(row=1, column=0, sticky="", padx=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def affiche_resultat(self, force_attaque, force_defense, joueur_attaque):
        attaque_echouee = ("L'ennemi a repoussé votre attaque!",
                           "Votre armée ne parvient pas à envahir le territoire",
                           "Vous n'aviez aucune chance face aux troupes de l'ennemi ",
                           "Malgré vos efforts, l'ennemi vous empêche d'envahir"
                           )
        attaque_reussie = ("Vous avez envahie le territoire avec succès!",
                           "L'ennemi n'avait aucune chance face à votre armée",
                           "Vous écrasez les forces ennemies sans difficulté",
                           "Vos forces militaires réussisent à combattre l'ennemi"
                           )

        force_egal = ("Malgré vos efforts, l'ennemi vous empêche de fanchir la frontière",
                      "Les forces de l'ennemi parvient de justesse à repousser votre attaque",
                      "Les forces militaires de l'ennemi étaient prêt à repousser votre attaque",
                      "Vous parvenez presque à réussir votre attaque")

        if isinstance(joueur_attaque, JoueurHumainTk):
            if force_attaque > force_defense:
                self.label_resultat['text'] = choice(attaque_reussie)
            elif force_attaque == force_defense:
                self.label_resultat['text'] = choice(force_egal)
            else:
                self.label_resultat['text'] = choice(attaque_echouee)
        else:
            self.label_resultat['text'] = ""

    def afficher_message(self, message):
        self.label_resultat["text"] = message

class FrameJoueurActif(Frame):
    def __init__(self, parent, joueurs):
        """
        Constructeur de la classe FrameJoueurActif. Affiche les informations relatives au
        joueur dont c'est le tour.

        Args:
            parent (Tk): La fenêtre dans laquelle ce frame s'insert.
        """

        super().__init__(parent)
        self.parent = parent
        self.joueurs = joueurs  # Les joueurs disponibles
        self.joueur_energie = {} # Dict Joueur : 0   (énergie qui s'additionne à la fin de chaque tour)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.label_affichage = Label(self)
        self.frame_affichage_joueur = Frame(self)
        self.frame_affichage_joueur.grid(row=0, column=0, columnspan=3)
        self.labels_joueurs = []
        for joueur in range(len(self.joueurs)):
            if __parametres__.get("easter_eggs"):
                try:
                    nom = __nom_pour_le_fun__[joueur]
                except:
                    nom = "Joueur " + str(joueur + 1)
            else:
                nom = "Joueur " + str(joueur + 1)
            self.labels_joueurs.append(Label(self.frame_affichage_joueur, text=nom,
                                             font=("Winden", 14), relief='sunken', width=10))
            self.labels_joueurs[joueur].grid(row=0, column=joueur, padx=10, pady=10)

        self.frame_affichage_option = Frame(self)
        self.frame_affichage_option.grid(row=1, column=0)
        self.label_des_surplus_fixe = Label(self.frame_affichage_option, text="Dés en surplus: ", font=("Arial", 12))
        self.label_des_surplus_variable = Label(self.frame_affichage_option, text="0", font=("Arial", 12))
        self.bouton = Button(self.frame_affichage_option, text="-", width=20, command=self.clic_bouton,
                             font=("Arial", 12))
        self.bouton_recommencer = Button(self.frame_affichage_option, text="Recommencer", width=20, font=("Arial", 12),
                                         command=self.recommencer)
        self.scale = tkinter.Scale(self.frame_affichage_option, orient=tkinter.HORIZONTAL, from_=10, to=500,
                                   font=("Arial", 12))
        self.label_affichage.grid(row=0, column=0)

        self.label_des_surplus_fixe.grid(row=2, column=0)
        self.label_des_surplus_variable.grid(row=2, column=1)
        self.bouton.grid(row=2, column=2, padx=10)
        self.bouton_recommencer.grid(row=3, column=2, padx=10)
        self.scale.grid(row=3, column=0)
        self.scale.set(TEMPS_ATTENTE)

        # initialisation de la musique
        self.compteur = 0
        mixer.init()
        mixer.music.load(liste_musics[self.compteur])
        mixer.music.play(loops=-1)
        mixer.music.set_volume(50)
        mixer.music.pause()
        self.audio = Button(self.frame_affichage_option, text="🎵",
                     relief=GROOVE, command=self.parametre_audio)
        self.audio.grid(row=2, column=3)

    def parametre_audio(self):
        x, y = self.audio.winfo_rootx(), self.audio.winfo_rooty()
        musique = FenetreAudio(x, y)
        musique.mainloop()

    def recommencer(self):
        """
        Permet à l'utilisateur de recommencer le jeu
        """
        self.master.destroy()
        canvas = self.parent.canvas_carte;
        for after_id in self.parent.eval('after info').split():
            canvas.after_cancel(after_id)
        FenetrePrincipale()

    def populer(self, joueur):
        """
        Cette méthode affiche les informations du joueur actif.

        Args:
            joueur (Joueur): le joueur actif
        """
        self.joueur_actif = joueur
        position_joueur = self.joueurs.index(joueur)
        for i in range(len(self.joueurs)):
            if i == position_joueur:
                self.labels_joueurs[i]['bg'] = joueur.couleur
                self.labels_joueurs[i]['relief'] = "raised"
            else:
                self.labels_joueurs[i]['bg'] = 'white'
                self.labels_joueurs[i]['relief'] = "sunken"

        self.label_des_surplus_variable['text'] = str(len(joueur.des_en_surplus))
        self.bouton['state'] = 'disable'

    def clic_bouton(self):
        """
        Cette méthode engendre la fin du tour.
        """
        self.sur_fin_tour(None)

    def energie(self, joueur):          # Méthode pour l'énergie des joueurs
        """
        Cee méthode donne de l'énergie à la fin de chaque tour.
        Args:
            joueur:
        """
        if joueur != None:
            if joueur.type_joueur == "Humain":
                try:
                    joueur.joueur_energie += 1
                except:
                    joueur.joueur_energie = 1
                if joueur.joueur_energie % int(__parametres__.get("red_bull_required")) == 0:
                    joueur.attaques_en_banque += 1
                self.parent.energy_bar.updateBar(joueur)

    def energie_show(self, joueur):
        self.parent.energy_bar.show(joueur)

    def energie_hide(self, joueur):
        self.parent.energy_bar.hide(joueur)

    def permettre_fin_tour(self, suite):
        """
        Cette méthode active le bouton de fin du tour.

        Args:
            suite (function): La fonction à exécuter lorsqu'on clique sur le bouton.
        """
        self.bouton['state'] = 'normal'
        self.bouton['text'] = 'Terminer le tour'
        self.sur_fin_tour = suite

    def permettre_annuler_selection(self, suite):
        """
        Cette méthode active le bouton qui annule le choix de l'attaquant.

        Args:
            suite (function): La fonction à exécuter lorsqu'on clique sur le bouton.
        """
        self.bouton['state'] = 'normal'
        self.bouton['text'] = 'Annuler la sélection'
        self.sur_fin_tour = suite

class FenetrePrincipale(Tk):
    def __init__(self):
        """
        Constructeur de la classe FenetrePrincipale.
        Cette classe gère l'instance de Guerre des dés, les joueurs et la carte.
        """
        super().__init__()
        self.tk_setPalette(background=BG_COLOR, foreground=FG_COLOR)

        self.title("Guerre des dés")
        self.label_bienvenue = Label(text="Bienvenue à la Guerre des dés!")

        path = "GuerresDesDesLogos.png"
        image = Image.open(path)
        image = image.resize((300, 153))
        img = ImageTk.PhotoImage(image)
        label = Label(self, image=img, borderwidth=0)
        label.photo = img
        label.grid(row=0, column=0, padx=20, pady=20)
        self.image_label = label

        self.bouton_commencer = ButtonCoinsRonds(self, bg="#1772e3", borderRadius=15, height=50, width=200, text="PRÉPARER LA PARTIE", fill="white", font="Helvetica 12 bold")
        def wrapper(event):
            self.lancer_fenetre_introduction()
        self.bouton_commencer.bind("<Button>", wrapper)
        #self.bouton_commencer.bind("<Enter>", self.bouton_commencer.grow)
        #self.bouton_commencer.bind("<Leave>", self.bouton_commencer.shrink)
        self.bouton_commencer.grid(row=3, column=0)

        self.project_label = Label(text="Jacob Robert-Charbonneau\nAndré Timotheatos\nRaphaël Arteau", font="Helvetica 10", fg="white")
        self.project_label.grid(row=4, column=0,pady=20)
        self.eval('tk::PlaceWindow . center')

        #self.bouton_commencer = Button(text="Commencer", width=20, command=self.lancer_fenetre_introduction)
        #self.label_bienvenue.grid(row=0, column=0, padx=10, pady=10)
        #self.bouton_commencer.grid(row=1, column=0, padx=10, pady=10)

    def lancer_fenetre_introduction(self):
        #self.tk_setPalette(background="White")
        fenetre_introduction = FenetreIntroduction(self)
        self.wait_window(fenetre_introduction)
        carte, joueurs = fenetre_introduction.obtenir_donnees()
        if carte is not None and joueurs is not None:
            self.demarrer(carte, joueurs)

    def demarrer(self, carte, joueurs):
        """
        Lance une partie.

        Args:
            carte (Carte): La carte de la partie
            joueurs (list): La liste des joueurs
        """
        desactiver_affichage()
        self.image_label.destroy()
        self.label_bienvenue.destroy()
        self.project_label.destroy()
        self.bouton_commencer.destroy()

        self.guerre_des_des = GuerreDesDes(joueurs, carte)
        self.joueurs = joueurs
        self.carte = carte

        carte.diviser_territoires(joueurs)
        self.update()

        self.resizable(False, False)
        self.canvas_carte = CanvasCarte(self, carte, self.winfo_screenheight())
        if __parametres__.get("red_bull"):
            un_joueur_humain = False
            for joueur in joueurs:
                if joueur.type_joueur == "Humain":
                    un_joueur_humain = True
                    break
            if un_joueur_humain:
                self.energy_bar = EnergyBar(self, joueurs)
                self.energy_bar.pack(side=RIGHT, fill="y")
        self.canvas_carte.pack(padx=20, pady=(10, 10))

        self.frame_attaque = FrameAttaque(self)
        self.frame_attaque.pack()
        self.frame_message = FrameMessage(self)
        self.frame_message.pack()
        self.frame_joueur = FrameJoueurActif(self, joueurs)  # Ajouter argument joueurs
        self.frame_joueur.pack(pady=(0,10))
        self.joueur_index = 0
        self.joueur_actuel = joueurs[self.joueur_index]
        if __parametres__.get("red_bull"):
            if self.joueur_actuel.type_joueur == "Humain":
                self.frame_joueur.energie_show(self.joueur_actuel)
        self.deroulement_debut_tour()

    def incrementer_joueur(self):
        """
        Cette méthode permet de passer au prochain joueur.
        """
        self.joueur_index = (self.joueur_index + 1) % len(self.joueurs)
        self.joueur_actuel = self.joueurs[self.joueur_index]
        while self.joueur_actuel.sauter_tour:
            messagebox.showinfo("Information", "Le joueur "+str(self.joueur_actuel.couleur)+" saute son tour!")
            self.joueur_actuel.sauter_tour = False
            self.joueur_index = (self.joueur_index + 1) % len(self.joueurs)
            self.joueur_actuel = self.joueurs[self.joueur_index]
        if __parametres__.get("red_bull"):
            if self.joueur_actuel.type_joueur == "Humain":
                self.frame_joueur.energie_show(self.joueur_actuel)

    def est_joueur_ordi(self):
        """
        Cette méthode indique s'il s'agit d'un joueur ordinateur

        Returns:
            bool: True s'il s'agit d'un ordinateur, False si joueur humain
        """
        return isinstance(self.joueur_actuel, JoueurOrdinateur)

    def redessiner(self, suite):
        """
        Cette méthode active le redessinage de la carte, et déclenche
        la suite.

        Args:
            suite (fonction): La fonction à exécuter suite au redessinage
        """

        self.canvas_carte.dessiner_canvas(self.joueur_actuel)

        if self.est_joueur_ordi():
            temps_attente = self.frame_joueur.scale.get()
        else:
            temps_attente = 0
        self.after(temps_attente, suite)
        # self.after(500, self.frame_attaque.vider())

    def afficher_joueur(self, joueur, suite):
        """
        Cette méthode affiche le joueur en cours

        Args:
            joueur (Joueur): Le joueur à afficher
            suite (fonction): La fonction à exécuter suite à l'affichage du joueur
        """
        self.frame_joueur.populer(joueur)
        self.redessiner(suite)

    def afficher_attaque(self, joueur_attaque, force_attaque, joueur_defense, force_defense, suite):
        """
        Cette méthode permet d'afficher les informations sur une attaque. <

        Args:
            joueur_attaque: Le joueur qui attaque
            force_attaque: La somme des dés de l'attaquant
            joueur_defense: Le joueur qui se défend
            force_defense: La somme des dés du défenseur
            suite (fonction): La fonction à exécuter suite à l'affichage
        """
        self.frame_attaque.populer(joueur_attaque, force_attaque, joueur_defense, force_defense)
        self.frame_message.affiche_resultat(force_attaque, force_defense, joueur_attaque)
        self.after(TEMPS_ATTENTE, lambda: self.redessiner(suite))

    def deroulement_debut_tour(self):
        """
        DÉROULEMENT, partie 1.
        Débute le tour
        """
        if self.est_joueur_ordi():
            self.canvas_carte.permettre_clics(None)
        self.afficher_joueur(self.joueur_actuel, self.deroulement_choix_attaquant)

    def deroulement_choix_attaquant(self):
        """
        DÉROULEMENT, partie 2.
        Permet le choix de l'attaquant.
        """
        if self.guerre_des_des.partie_terminee():
            self.afficher_gagnant()
        else:
            self.carte.tout_deselectionner()
            if self.est_joueur_ordi():
                attaquant = self.joueur_actuel.selectionner_attaquant(self.carte)
                self.deroulement_fin_selection_attaquant(attaquant)
            else:
                self.frame_joueur.permettre_fin_tour(lambda _: self.deroulement_fin_selection_attaquant(None))
                self.canvas_carte.permettre_clics(lambda coor:
                                                  self.deroulement_choix_attaquant_humain(coor))

    def deroulement_choix_attaquant_humain(self, coor):
        """
        DÉROULEMENT, partie 3.
        Permet le choix de l'attaquant par un joueur humain

        Args:
            coor (tuple): Les coordonnées sur lesquelles on a cliqué
        """
        attaquant = self.joueur_actuel.selectionner_attaquant(self.carte, coor)
        if attaquant is None:
            self.deroulement_choix_attaquant()
        else:
            self.deroulement_fin_selection_attaquant(attaquant)

    def deroulement_fin_selection_attaquant(self, attaquant):
        """
        DÉROULEMENT, partie 4.
        Termine le tour ou permet de choisir un défenseur.

        Args:
            attaquant (Case): La case qui attaque. Si None, c'est la fin du tour.
         """
        if attaquant is None:
            if __parametres__.get("red_bull"):
                self.frame_joueur.energie(self.joueur_actuel)
            self.guerre_des_des.fin_du_tour(self.joueur_actuel)
            self.incrementer_joueur()
            self.deroulement_debut_tour()
        else:
            self.redessiner(lambda: self.deroulement_choix_defenseur(attaquant))

    def deroulement_choix_defenseur(self, attaquant):
        """
        DÉROULEMENT, partie 5.
        Permet de choisir le défenseur.

        Args:
            attaquant (Case): la case qui attaque
        """
        if self.est_joueur_ordi():
            defenseur = self.joueur_actuel.selectionner_defenseur(self.carte, attaquant)
            self.redessiner(self.deroulement_choix_defenseur_fin(attaquant, defenseur))
        else:
            suite = lambda coor_def: self.deroulement_choix_defenseur_humain(attaquant, coor_def)
            self.frame_joueur.permettre_annuler_selection(suite)
            self.canvas_carte.permettre_clics(suite)

    def deroulement_choix_defenseur_humain(self, attaquant, coor_def):
        """
        DÉROULEMENT, partie 6.
        Séelectionne la case en fonction des coordonnées.

        Args:
            attaquant (Case): la case qui attaque.
            coor_def (tuple): les coordonnées de la case sélectionnée pour défense
        """
        defenseur = self.joueur_actuel.selectionner_defenseur(self.carte, attaquant, coor_def)
        if attaquant is None:
            self.deroulement_choix_attaquant()
        else:
            self.redessiner(self.deroulement_choix_defenseur_fin(attaquant, defenseur))

    def deroulement_choix_defenseur_fin(self, attaquant, defenseur):
        """
        DÉROULEMENT, partie 7.
        Annule le choix de l'attaquant ou effectue une attaque.

        Args:
            attaquant (Case): La case qui attaque.
            defenseur (Case): La case qui se défend. Si None on retourne au choix de l'attaquant.

        Returns:

        """
        if defenseur is None:
            self.deroulement_choix_attaquant()
        else:
            self.redessiner(lambda: self.deroulement_attaque(attaquant, defenseur))

    def deroulement_attaque(self, attaquant, defenseur):
        """
        DÉROULEMENT, partie 8.
        Effectue une attaque.

        Args:
            attaquant (Case): La case qui attaque
            defenseur (Case): La case qui se défend
        """
        defenseur_appartenance_avant = defenseur.appartenance
        force_attaquant, force_defenseur = self.guerre_des_des.attaquer(attaquant, defenseur)
        self.carte.tout_deselectionner()
        if force_attaquant > force_defenseur:
            if __parametres__.get("red_bull"):
                self.frame_joueur.energie(self.joueur_actuel)
        self.afficher_attaque(attaquant.appartenance, force_attaquant,
                              defenseur_appartenance_avant, force_defenseur,
                              self.deroulement_choix_attaquant)

    def afficher_gagnant(self):
        """
        Affiche le gagnant de la partie.
        """
        gagnant = self.guerre_des_des.determiner_gagnant()
        messagebox.showinfo("Fin de la partie", "Victoire du joueur " + couleurs_interface[gagnant.couleur])
        self.canvas_carte.permettre_clics(None)
        self.frame_joueur.populer(gagnant)
        restart = messagebox.askquestion("Nouvelle partie", "Voulez-vous commencer une nouvelle partie ?")
        if restart == 'yes':
            self.destroy()
            FenetrePrincipale()
        else:
            quit()
