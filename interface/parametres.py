import json
import tkinter
from tkinter import *


__nom_pour_le_fun__ = [
    "Skrou",
    "Louis",
    "André",
    "Jacob",
    "Raphaël"
]

class Parametres():
    def __init__(self):
        """
        Le constructeur de la calsse parametre va chercher pour une fichier texte
        setting.txt

        Le fichier contient une string en format JSON contenant les paramètre
        voulant être sauvegardées.

        Args:
            Aucun
        """
        self.default_settings = {
            "zoom_recursif": True,
            "bg_color": "#076AE1",
            "fg_color": "black",
            "red_bull" : False,
            "red_bull_required" : 10,
            "advanced_player_control" : False,
            "war_mode" : False,
            "easter_eggs" : False,
            "aide_prob" : False
        }
        self.settingsSession = {}
        try:
            f = open("setting.txt")
            self.settings = json.loads(f.readlines()[0])
        except Exception as e:
            self.updateFile(self.default_settings)
        reupdate = False

        """
        Le code ci-dessous compare les paramètres du fichier setting.txt et 
        les compare avec les paramètres par default, si le parametre n'existe pas
        dans le fichier, on le prend des parametres par default
        """
        for setting in self.default_settings:
            try:
                self.settings
            except:
                self.settings = {}
            if setting not in self.settings:
                self.settings[setting] = self.default_settings[setting]
                reupdate = True
        if reupdate:
            self.updateFile(self.settings)

    def get(self, name):
        if name in self.settingsSession:
            return self.settingsSession[name]
        elif name in self.settings:
            return self.settings[name]
        else:
            return False

    def set(self, name, value, **args):
        self.settings[name] = value
        self.updateFile(self.settings)
        if "command" in args:
            if "commande_args" not in args:
                args["command_args"] = {}
                try:
                    args["command"](args["command_args"])
                except:
                    pass
            else:
                args["command"]()

    def setSession(self, name, value):
        self.settingsSession[name] = value

    def bulkSet(self, dic):
        for name, value in dic.items():
            self.settings[name] = value
        self.updateFile(self.settings)

    def updateFile(self, settings):
        f = open("setting.txt", "w")
        f.write(json.dumps(settings))
        f.close()

    def help(self):
        print("Fonctions fournies dans Parametres() : ")
        print("Parametres().get(name) -> Le nom du parametre a obtenir, priorise les parametres session sur les parametres sauvegardés.")
        print("Parametres().set(name, value) -> Le nom du parametre a changer ou créer ainsi que sa valeur.")
        print("Parametres().setSession(name, value) -> Créer ou changer un parametre pour la session actuelle, ne sera pas sauvegardé pour une prochaine session.")
        print("Parametres().bulkSet(dictionnary) -> Fait un set sur chaque element du dictionnaire puis update le fichier setting.txt")



__parametres__ = Parametres()
BG_COLOR = __parametres__.get("bg_color")
FG_COLOR = __parametres__.get("fg_color")
FRAME_COLOR = "white"

class FenetreParametres(Toplevel):
    def __init__(self, parent, largeur, hauteur):
        super().__init__(parent)
        self.parent = parent
        self.transient(parent)
        self.grab_set()
        self.largeur = largeur
        self.hauteur = hauteur

        self.configure(bg="white")
        self.fenetre_parametre_position()
        self.title("Paramètres Avancés")

        """
        if __parametres__.get("Advanced_Player_Choice"):
            value = 1
        else:
            value = 0
        self.advance_player_control = IntVar(value=value)
        self.checkbox_advance_player_control = Checkbutton(self, text="Contrôle des joueurs avancé", variable=self.advance_player_control)
        self.checkbox_advance_player_control.grid(row=0, column=0,padx = 5, pady = 5)
        """

        if __parametres__.get("zoom_recursif"):
            value = 1
        else:
            value = 0
        self.zoom_recursif = IntVar(value=value)
        self.zoom_recursif_button = Checkbutton(self, text="Zoom Recursif",variable=self.zoom_recursif)
        self.zoom_recursif_button.pack(pady=5, padx=10, anchor='w')

        frame = Frame(self)
        if __parametres__.get("red_bull"):
            value_red_bull = 1
        else:
            value_red_bull = 0
        self.red_bull = IntVar(value=value_red_bull)
        self.red_value_nombre = StringVar()
        self.red_value_nombre.set(__parametres__.get("red_bull_required"))
        self.red_bull_entry = Entry(frame, width=3, textvariable=self.red_value_nombre, highlightbackground="white")
        self.red_bull_button = Checkbutton(frame, text="Énergie et Attaques Spéciales  -",variable=self.red_bull, command=lambda elem=self.red_bull_entry:self.disableEnable(elem))
        self.red_bull_button.pack(side="left", pady=5, padx=(10,0), anchor='w')
        red_bull_label_one = Label(frame, text="Après")
        red_bull_label_two = Label(frame, text="bon coups")
        if not __parametres__.get("red_bull"):
            self.red_bull_entry["state"] = 'disabled'
        red_bull_label_one.pack(side="left", pady=5, padx=0)
        self.red_bull_entry.pack(side="left", pady=5, padx=0)
        red_bull_label_two.pack(side="left", pady=5, padx=(0,10))
        frame.pack()

        if __parametres__.get("advanced_player_control"):
            value_advanced_player_control = 1
        else:
            value_advanced_player_control = 0
        self.advanced_player_control = IntVar(value=value_advanced_player_control)
        self.advanced_player_control_button = Checkbutton(self, text="Contrôle avancé des joueurs",variable=self.advanced_player_control)
        self.advanced_player_control_button.pack(pady=5, padx=10, anchor='w')

        if __parametres__.get("aide_prob"):
            value = 1
        else:
            value = 0
        self.aide_prob_value = IntVar(value=value)
        self.aide_prob_button = Checkbutton(self, text="Montrer probabilitées d'attaques gagnantes",variable=self.aide_prob_value)
        self.aide_prob_button.pack(pady=5, padx=10, anchor='w')

        if __parametres__.get("war_mode"):
            war_mode_value_1 = 1
        else:
            war_mode_value_1 = 0
        self.war_mode_value = IntVar(value=war_mode_value_1)
        if __parametres__.get("easter_eggs"):
            self.war_mode_button = Checkbutton(self, text="Mode Michael Bay",variable=self.war_mode_value)
        else:
            self.war_mode_button = Checkbutton(self, text="Mode Guerre", variable=self.war_mode_value)
        self.war_mode_button.pack(pady=5, padx=10, anchor='w')

        if __parametres__.get("easter_eggs"):
            easter_eggs_value = 1
        else:
            easter_eggs_value = 0
        self.easter_eggs_value_intvar = IntVar(value=easter_eggs_value)
        self.easter_eggs_button = Checkbutton(self, text="Mode Easter Eggs",variable=self.easter_eggs_value_intvar)
        self.easter_eggs_button.pack(pady=5, padx=10, anchor='w')

        """
        self.taille_case = Label(self, text="Taille minimum de case (px)")
        self.min_taille_case = StringVar()
        self.min_taille_case.set(__parametres__.get("min_taille_case"))
        self.taille_case_entry = Entry(self, width=5, textvariable=self.min_taille_case)
        self.taille_case.grid(row=1, column=0)
        self.taille_case_entry.grid(row=1, column=1)
        """

        frame = Frame(self)
        self.bouton_commencer = Button(frame, text="Fermer", command=self.fermer, highlightbackground="white", bg="white")
        self.bouton_commencer.grid(row=0, column=0, padx=4, pady=4)

        self.bouton_parametres = Button(frame, text="Sauvegarder", command=self.sauvegarder,highlightbackground="white")
        self.bouton_parametres.grid(row=0, column=1, padx=4, pady=4)
        frame.pack()

        def whiteBG(element):
            try:
                element.configure(bg=FRAME_COLOR)
                children = element.winfo_children()
                for child in children:
                    pass
                    whiteBG(child)
            except:
                pass
        whiteBG(self)

    def fermer(self):
        self.destroy()

    def disableEnable(self, elem):
        if elem["state"] != 'disabled':
            elem["state"] = 'disabled'
        else:
            elem["state"] = 'normal'

    def sauvegarder(self):
        __parametres__.bulkSet({
            "zoom_recursif": self.zoom_recursif.get(),
            "red_bull": self.red_bull.get(),
            "red_bull_required": self.red_value_nombre.get(),
            "advanced_player_control" : self.advanced_player_control.get(),
            "war_mode": self.war_mode_value.get(),
            "easter_eggs" : self.easter_eggs_value_intvar.get(),
            "aide_prob" : self.aide_prob_value.get()
        })
        self.parent.regen()
        self.destroy()

    def fenetre_parametre_position(self):
        """
        Permet de centrer la fenêtre un milieu de l'écran
        """
        self.update()
        x_coor = int(self.largeur + self.winfo_reqwidth()/2.8)
        y_coor = int(self.hauteur + self.winfo_reqheight()/1.5)
        #self.geometry(f'+{int(y_coor)}+{x_coor}')
        self.parent.parent.eval(f'tk::PlaceWindow {str(self)} center')
