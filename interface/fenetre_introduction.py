"""
Module contenant la classe FenetreIntroduction et ses classes
utilitaires FrameCarte et FrameJoueurs.
"""
import random
import platform
from tkinter import IntVar, Radiobutton, Button, Label, Entry, Frame, filedialog, END, messagebox, RIDGE, Toplevel

from guerre_des_des_tp3.afficheur import couleurs_interface
from guerre_des_des_tp3.carte_autogeneree import CarteAutogeneree
from ia.ai_jacob import JoueurOrdinateurAmelioreJacob
from ia.ai_raph import JoueurOrdinateurRaph
from ia.joueur_ordinateur_ameliore import JoueurOrdinateurAmeliore
from interface.carte_televersee import CarteTeleversee
from interface.elements_tkinter_perso import ButtonCoinsRonds
from interface.joueur_humain_tk import JoueurHumainTk
from interface.parametres import FenetreParametres, FRAME_COLOR, __parametres__
from PIL import ImageTk, Image

MAXIMUM = 20
MINIMUM = 2


class FrameCarte(Frame):
    def __init__(self, parent):
        """
        Constructeur de la classe FrameCarte. Cette classe gère le menu
        de création de carte. Soit par dimensions (CarteAutogeneree) ou avec un
        fichier (CarteTeleversee).

        Args:
            parent (Frame): Le widget TKinter dans lequel la frame s'intègre.
        """
        super().__init__(parent, borderwidth=1, relief=RIDGE, bg="#1772e3")

        self.choix_mode = IntVar()
        self.hauteur_var = IntVar()
        self.largeur_var = IntVar()
        self.nb_trous_var = IntVar()
        self.hauteur_var.set(5)
        self.largeur_var.set(5)
        self.nb_trous_var.set(4)

        self.radio_generer = Radiobutton(self, text="Générer une carte",
                                         variable=self.choix_mode, value=1,
                                         command=self.selection_mode,bg="#1772e3", fg="white", selectcolor='#1772e3',
                                         font="Winden")
        self.radio_aleatoire = Radiobutton(self, text="Générer une carte aléatoire",
                                           variable=self.choix_mode, value=3,
                                           command=self.selection_mode,bg="#1772e3", selectcolor='#1772e3', fg="white",
                                           font="Winden")
        self.radio_importer = Radiobutton(self, text="Importer une carte",
                                          variable=self.choix_mode, value=2,
                                          command=self.selection_mode, bg="#1772e3", selectcolor='#1772e3', fg="white",
                                          font="Winden")

        self.frame_generer = Frame(self,bg="#1772e3")
        self.label_hauteur = Label(self.frame_generer, text="Hauteur: ", bg="#1772e3", fg="white",  font="Winden")
        self.label_hauteur_max = Label(self.frame_generer, text="(2-20)", bg="#1772e3", fg="white",  font="Winden")
        self.label_verifier_hauteur = Label(self.frame_generer, text="✓", font=12, fg="lime green", bg="#1772e3")
        self.entry_hauteur = Entry(self.frame_generer, width=5, textvariable=self.hauteur_var, bg="#1772e3",
                                   highlightbackground="white", fg="white",  font="Winden")

        self.label_largeur = Label(self.frame_generer, text="Largeur: ",bg="#1772e3", fg="white",  font="Winden")
        self.entry_largeur = Entry(self.frame_generer, width=5, textvariable=self.largeur_var,bg="#1772e3",
                                   highlightbackground="white", fg="white",  font="Winden")
        self.label_largeur_max = Label(self.frame_generer, text="(2-20)", bg="#1772e3", fg="white",  font="Winden")
        self.label_verifier_largeur = Label(self.frame_generer, text="✓", font=12, fg="lime green",bg="#1772e3")
        self.label_nb_trous = Label(self.frame_generer, text="Nombre de trous: ",bg="#1772e3", fg="white",  font="Winden")
        self.label_verifier_nb_trous = Label(self.frame_generer, text="✓", font=12, fg="lime green",bg="#1772e3")
        self.entry_nb_trous = Entry(self.frame_generer, width=5, textvariable=self.nb_trous_var, bg="#1772e3",
                                    highlightbackground="white", fg="white",  font="Winden")

        self.label_hauteur.grid(row=0, column=0,  sticky='w')
        self.entry_hauteur.grid(row=0, column=1)
        self.label_hauteur_max.grid(row=0, column=3)
        self.label_verifier_hauteur.grid(row=0, column=4)

        self.label_largeur.grid(row=1, column=0, sticky='w')
        self.entry_largeur.grid(row=1, column=1)
        self.label_largeur_max.grid(row=1, column=3)
        self.label_verifier_largeur.grid(row=1, column=4)

        self.label_nb_trous.grid(row=2, column=0,  sticky='w')
        self.entry_nb_trous.grid(row=2, column=1)
        self.label_verifier_nb_trous.grid(row=2, column=4)

        self.frame_importer = Frame(self, bg="#1772e3")
        self.entry_fichier = Entry(self.frame_importer, text="", bg='white')
        self.bouton_fichier = Button(self.frame_importer, text="Sélectionner...", foreground="black",
                                     command=self.choisir_fichier, bg="#2d7fe4", highlightbackground="white",
                                     font="winden", fg="white")
        self.bouton_fichier.grid(row=0, column=0, padx=5, pady=5)
        self.entry_fichier.grid(row=0, column=1, padx=5, pady=5)


        self.radio_generer.grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.frame_generer.grid(row=2, column=0, padx=5, pady=2)
        self.radio_importer.grid(row=3, column=0, padx=5, pady=2, sticky="w")
        self.frame_importer.grid(row=4, column=0, padx=5, pady=2, sticky="w")
        self.radio_aleatoire.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        if __parametres__.get("easter_eggs"):
            self.carte_speciale_option = Radiobutton(self, text="Utiliser une carte spéciale",
                                              variable=self.choix_mode, value=4,
                                              command=self.selection_mode, fg="white", bg="#1772e3")
            self.carte_speciale_option.grid(row=5, column=0, padx=5, pady=2, sticky="w")
        self.choix_mode.set(1)
        self.selection_mode()

    def obtenir_valeurs(self, hauteur, largeur, nb_trous):
        self.hauteur = hauteur
        self.largeur = largeur
        self.nb_trous = nb_trous

    def choisir_fichier(self):
        """
        Cette méthode ouvre une fenêtre de dialogue pour choisir un fichier
        et met inscrit le nom du fichier choisi dans la zone dédiée à cette fin.
        """
        self.entry_fichier.delete(0, END)
        self.entry_fichier.insert(0, filedialog.askopenfilename())

    def selection_mode(self):
        """
        Cette méthode gère le mode de choix de carte, en fonction des boutons radio.
        """
        if self.choix_mode.get() == 1:
            mode_importer = 'disable'
            mode_generer = 'normal'
        elif self.choix_mode.get() == 3 or self.choix_mode.get() == 4:
            mode_importer = 'disable'
            mode_generer = 'disable'
        else:
            mode_importer = 'normal'
            mode_generer = 'disable'
        for child in self.frame_importer.winfo_children():
            child.configure(state=mode_importer)
        for child in self.frame_generer.winfo_children():
            child.configure(state=mode_generer)

    def obtenir_carte(self):
        """
        Cette méthode crée une carte en fonction des paramètres déterminés dans le frame.

        Returns:
            carte: La carte créée.
        """

        if self.choix_mode.get() == 1:
            # try:

            hauteur = self.hauteur
            largeur = self.largeur
            nb_trous = self.nb_trous

            return CarteAutogeneree(hauteur, largeur, nb_trous)
        elif self.choix_mode.get() == 3:
            while True:
                hauteur = random.randint(MINIMUM, MAXIMUM)
                largeur = random.randint(MINIMUM, MAXIMUM)
                nb_trous = random.randint(1, (hauteur * largeur) // 4)
                if not (hauteur / largeur < 0.4 or largeur / hauteur < 0.4):
                    return CarteAutogeneree(hauteur, largeur, nb_trous)
        elif self.choix_mode.get() == 4:
            nom_fichier = "ift-1004_final.txt"
            return CarteTeleversee(nom_fichier)
        else:
            nom_fichier = self.entry_fichier.get()
            return CarteTeleversee(nom_fichier)


class FrameJoueurs(Frame):
    def __init__(self, parent):
        """
        Constructeur de la classe FrameJoueurs. Cette classe gère le menu
        du choix des joueurs.

        Args:
            parent (Frame): Le widget TKinter dans lequel la frame s'intègre.
        """
        super().__init__(parent, borderwidth=1, relief=RIDGE, bg="#1772e3")
        label_joueurs = Label(self, text="Sélectionnez les joueurs", bg="#1772e3", fg="white",  font="Winden")
        label_joueurs.grid(row=0, column=0, padx=10, pady=10)
        self.label_joueurs_valide = Label(self, text="", bg="#1772e3", font='Winden', fg="white")
        self.label_joueurs_valide.grid(row=3, column=0, pady=13)
        self.boutons_joueur = []
        self.boutons_dif = []
        self.couleurs = list(couleurs_interface.keys())
        frame_boutons = Frame(self, bg="#1772e3")
        self.advanced = __parametres__.get("advanced_player_control")
        os = platform.system()
        text_color = "white"
        if os == "Darwin":
            text_color = "black"
        if self.advanced:
            for i in range(3):
                bouton_joueur = Button(frame_boutons, text="Inactif", width=8, highlightbackground="white",
                                       font='sans 12',
                                       command=lambda c=i: self.changer_type_joueur(c))
                bouton_joueur.grid(row=i, column=0, padx=5, pady=5)
                bouton_joueur['background'] = self.couleurs[i]
                bouton_joueur.background_to_set = self.couleurs[i]
                bouton_joueur['activebackground'] = self.couleurs[i]
                bouton_dif = Button(frame_boutons, text="Facile", width=8, highlightbackground="white",
                                       font='sans 12',
                                       command=lambda c=i: self.changer_dif_joueur(c))
                bouton_dif["state"] = "disabled"
                bouton_dif.grid(row=i, column=1, padx=5, pady=5)
                self.boutons_joueur.append(bouton_joueur)
                self.boutons_dif.append(bouton_dif)
            self.boutons_joueur[0]['text'] = "Humain"
            self.boutons_joueur[1]['text'] = "Ordinateur"
            self.boutons_dif[1]["state"] = "active"
        else:
            for i in range(0, 3):
                bouton_joueur = Button(frame_boutons, text="Inactif", width=8, highlightbackground="white",
                                       fg=text_color, font='sans 12',
                                       command=lambda c=i: self.changer_type_joueur(c))
                bouton_couleur_joueur = Button(frame_boutons, width=3, bg='red', font=12, state='disable')
                bouton_joueur.grid(row=i, column=0, padx=5, pady=5)
                if os != "Darwin":
                    bouton_couleur_joueur.grid(row=i, column=1, padx=(0, 5), pady=5)
                bouton_couleur_joueur['background'] = self.couleurs[i]
                bouton_joueur.background_to_set = self.couleurs[i]
                self.boutons_joueur.append(bouton_joueur)
            for i in range(3, 6):
                bouton_joueur = Button(frame_boutons, text="Inactif", width=8, highlightbackground="white",
                                       fg=text_color, font='sans 12', command=lambda c=i: self.changer_type_joueur(c))
                bouton_couleur_joueur = Button(frame_boutons, width=3, bg='red', font=12, state='disable')
                bouton_joueur.grid(row=i-3, column=2, padx=5, pady=5)
                if os != "Darwin":
                    bouton_couleur_joueur.grid(row=i-3, column=3, padx=(0, 5), pady=5)
                bouton_couleur_joueur['background'] = self.couleurs[i]
                bouton_joueur.background_to_set = self.couleurs[i]
                self.boutons_joueur.append(bouton_joueur)
            self.boutons_joueur[0]['text'] = "Humain"
            self.boutons_joueur[1]['text'] = "Ordinateur"
        frame_boutons.grid(row=1, column=0)

    def obtenir_joueurs(self, carte):
        """
        Cette méthode crée les joueurs en fonction du contenu des boutons.

        Returns:
            list: La liste des joueurs
        """
        joueurs = []
        index = 0
        for bouton_joueur in self.boutons_joueur:
            if bouton_joueur['text'] == "Humain":
                joueurs.append(JoueurHumainTk(bouton_joueur.background_to_set))
            elif bouton_joueur['text'] == "Ordinateur":
                if self.advanced:
                    dif = self.boutons_dif[index]["text"]
                    if dif == "Facile":
                        joueurs.append(JoueurOrdinateurAmeliore(bouton_joueur.background_to_set, carte))
                    elif dif == "Moyenne":
                        joueurs.append(JoueurOrdinateurAmelioreJacob(bouton_joueur.background_to_set, carte))
                    elif dif == "Difficile":
                        joueurs.append(JoueurOrdinateurRaph(bouton_joueur.background_to_set, carte))
                else:
                    joueurs.append(JoueurOrdinateurAmeliore(bouton_joueur.background_to_set, carte))
            index += 1
        return joueurs

    def changer_dif_joueur(self, i):
        if self.boutons_dif[i]['text'] == "Facile":
            self.boutons_dif[i]['text'] = "Moyenne"
        elif self.boutons_dif[i]['text'] == "Moyenne":
            self.boutons_dif[i]['text'] = "Difficile"
        else:
            self.boutons_dif[i]['text'] = "Facile"

    def changer_type_joueur(self, i):
        """
        Cette fonction permet de modifier le contenu du bouton dont
        le numéro est en paramètres.

        Args:
            i (int): Le numéro du bouton à modifier
        """
        if self.boutons_joueur[i]['text'] == "Inactif":
            self.boutons_joueur[i]['text'] = "Humain"
            if self.advanced:
                self.boutons_dif[i]["state"] = "disabled"
        elif self.boutons_joueur[i]['text'] == "Humain":
            self.boutons_joueur[i]['text'] = "Ordinateur"
            if self.advanced:
                self.boutons_dif[i]["state"] = "normal"
        else:
            self.boutons_joueur[i]['text'] = "Inactif"
            if self.advanced:
                self.boutons_dif[i]["state"] = "disabled"


class FenetreIntroduction(Toplevel):
    def __init__(self, parent):
        """
        Constructeur de la classe FenetreIntroduction. Cette classe permet
        de choisir les paramètres de la partie et de démarrer la partie.
        """
        super().__init__(parent)
        self.parent = parent
        self.transient(parent)
        self.grab_set()

        self.title("Paramètres de la partie...")
        self.carte = None
        self.joueurs = None

        self.label_introduction = Label(self, text="Bienvenue à la Guerre des dés!")

        path = "GuerresDesDesLogos.png"
        image = Image.open(path)
        image = image.resize((200, 102))
        img = ImageTk.PhotoImage(image)
        label = Label(self, image=img, borderwidth=0)
        label.photo = img
        label.grid(row=0, column=0, padx=20, pady=20)
        self.image_label = label
        self.regen()

        #self.bouton_commencer = Button(self, text="Commencer!", command=self.commencer, fg="black")
        #self.bouton_commencer.grid(row=2, column=0, padx=10, pady=10)
        self.bouton_commencer = ButtonCoinsRonds(self, text="Commencer!",fill="white",bg="#1772e3",
                                                 font="Helvetica 20 bold", width=200, height=50, borderRadius=20)
        self.bouton_commencer.grid(row=2, column=0)
        self.update()
        self.bind("<Key>", self.validation_valeurs)
        self.bind("<Motion>", self.validation_valeurs)
        self.bind("<ButtonRelease>", self.validation_joueurs)
        self.fenetre_introduction_centre()

    def fenetre_introduction_centre(self):
        """
        Permet de centrer la fenêtre un milieu de l'écran
        """
        self.update()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coor = int((screen_width / 2) - (self.winfo_reqwidth() / 2))
        y_coor = int((screen_height / 2) - (self.winfo_reqheight() / 2))
        self.geometry(f'+{int(x_coor)}+{y_coor}')

    def validation_valeurs(self, event=None):
        """
        Permet à l'utilisateur de voir si les entrées sont valides
        Args:
            event: Aucune
        """
        try:
            hauteur = self.frame_carte.hauteur_var.get()
        except:
            hauteur = 0
        try:
            largeur = self.frame_carte.largeur_var.get()
        except:
            largeur = 0
        try:
            nb_trous = self.frame_carte.nb_trous_var.get()
        except:
            nb_trous = 0
        self.frame_carte.obtenir_valeurs(hauteur, largeur, nb_trous)
        if self.frame_carte.choix_mode.get() == 1:
            valeurs_ok = True
            if hauteur > MAXIMUM or hauteur < MINIMUM:
                self.frame_carte.label_verifier_hauteur["fg"] = "red"
                self.frame_carte.label_verifier_hauteur["text"] = "✘"
                valeurs_ok = False
            else:
                self.frame_carte.label_verifier_hauteur["fg"] = "lime green"
                self.frame_carte.label_verifier_hauteur["text"] = "✓"
            if largeur > MAXIMUM or largeur < MINIMUM:
                self.frame_carte.label_verifier_largeur["fg"] = "red"
                self.frame_carte.label_verifier_largeur["text"] = "✘"
                valeurs_ok = False
            else:
                self.frame_carte.label_verifier_largeur["fg"] = "lime green"
                self.frame_carte.label_verifier_largeur["text"] = "✓"
            if nb_trous == 0 or nb_trous > (hauteur * largeur) // 4:
                self.frame_carte.label_verifier_nb_trous["fg"] = "red"
                self.frame_carte.label_verifier_nb_trous["text"] = "✘"
                valeurs_ok = False
            else:
                self.frame_carte.label_verifier_nb_trous["fg"] = "lime green"
                self.frame_carte.label_verifier_nb_trous["text"] = "✓"
            self.valeurs_valides = valeurs_ok

        if self.frame_carte.choix_mode.get() == 2:
            if len(self.frame_joueurs.obtenir_joueurs(self.carte)) >= 2 and self.frame_carte.entry_fichier.get() != "":
                self.valeurs_valides = True
            else:
                self.valeurs_valides = False

        if self.frame_carte.choix_mode.get() == 3:
            if len(self.frame_joueurs.obtenir_joueurs(self.carte)) >= 2:
                self.valeurs_valides = True
            else:
                self.valeurs_valides = False

        if len(self.frame_joueurs.obtenir_joueurs(self.carte)) < 2:
            self.valeurs_valides = False

        def wrapper(event, self):
            self.commencer()
        if self.valeurs_valides:
            self.bouton_commencer.raphconfig({"bg": "#1772e3", "fill": "white"})
            self.bouton_commencer.bind("<Button>", lambda event,self=self:wrapper(event,self))
        else:
            self.bouton_commencer.raphconfig({"bg": "grey", "fill": "lightgrey"})
            self.bouton_commencer.unbind("<Button>")


    def regen(self):
        try:
            self.frame_frame.destroy()
        except:
            pass
        self.frame_frame = Frame(self)
        self.frame_carte = FrameCarte(self.frame_frame)
        self.frame_carte.grid(row=0, column=0, padx=10, pady=10)
        self.frame_joueurs = FrameJoueurs(self.frame_frame)
        self.frame_joueurs.grid(row=0, column=1, padx=10, pady=10)
        self.frame_frame.grid(row=1, column=0)
        self.genParamAvancee()

    def validation_joueurs(self, event=None):
        if len(self.frame_joueurs.obtenir_joueurs(self.carte)) < 2:
            self.frame_joueurs.label_joueurs_valide["text"] = "MINIMUM 2 JOUEURS"
        else:
            self.frame_joueurs.label_joueurs_valide["text"] = ""


    def genParamAvancee(self):
        try:
            self.param_button.destroy()
        except:
            pass
        if __parametres__.get("war_mode"):
            path = "grenade2.png"
            grenade = Image.open(path)
            h, l = grenade.size
            grenade = grenade.resize((h // 33, l // 33))
            self.photo_grenade = ImageTk.PhotoImage(grenade)
            self.param_button = Button(self, image=self.photo_grenade, relief="flat", command=self.param_avance)
        else:
            path = "settings.png"
            settings = Image.open(path)
            h, l = settings.size
            settings = settings.resize((h // 14, l // 14))
            self.photo_settings = ImageTk.PhotoImage(settings)
            self.param_button = Button(self, image=self.photo_settings, relief="flat", command=self.param_avance)
        self.param_button.grid(row=3,column=0, padx=10, pady=10, sticky="se")

    def commencer(self):
        """
        Cette méthode crée la fenêtre principale en fonction des paramètres dans les frames.
        """
        if self.valeurs_valides:
            try:
                self.carte = self.frame_carte.obtenir_carte()
                self.joueurs = self.frame_joueurs.obtenir_joueurs(self.carte)
                self.tk_setPalette(background="white")
                self.grab_release()
                # self.parent.configure(bg="White")
                self.parent.focus_set()
                self.destroy()

            except ValueError as e:
                messagebox.showerror("Erreur", str(e))

    def obtenir_donnees(self):
        return self.carte, self.joueurs

    def param_avance(self, event=False):
        self.fenetre_param = FenetreParametres(self, self.winfo_reqwidth(), self.winfo_screenheight())