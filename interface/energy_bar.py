from tkinter import Canvas, Toplevel, Label, Frame, Button, messagebox

from PIL import ImageTk, Image

from interface.elements_tkinter_perso import ButtonCoinsRonds
from interface.parametres import __parametres__, BG_COLOR, FG_COLOR


class EnergyBar(Canvas):
    def __init__(self, parent, joueurs):
        super().__init__(parent)
        self.parent = parent
        self.animQueue = []
        self.dernierButtonAttaque = None
        self.watch_mode = False
        self.joueurs = joueurs
        self.height = int(parent.canvas_carte.cget("height"))
        self.width = 130
        self.configure(width=self.width, height=self.height)
        self.create_text((self.width/2),(self.height+40),text="Énergie", font="Helvetica 18 bold")

        self.left = (self.width/2)-20
        self.right = (self.width/2)+20
        self.top = 20
        self.bottom = self.height
        self.create_rectangle(self.left,self.top,self.right,self.bottom,outline="black")

        self.buttonAnnuler = ButtonCoinsRonds(self, bg="blue", canvas_bg="white", borderRadius=15, height=70, width=120, text="Annuler\nAttaque", fill="white", font="Helvetica 13")
        self.buttonAnnuler.bind("<Button>", self.cancelAttack)

        for joueur in joueurs:
            joueur.joueur_energie = 0
            joueur.attaques_en_banque = 0
            joueur.bar = self.create_rectangle(self.left,self.bottom,self.right,self.bottom,fill=joueur.couleur, state="hidden")
            joueur.text_energie = self.create_text((self.width/2),(self.height+70),text="0",font="Helvetica 12 bold", state="hidden")
            joueur.button_attaque_speciale = ButtonCoinsRonds(self, bg="grey", canvas_bg="white", borderRadius=15, height=80, width=120,
                             text="💣 Attaques 💣\n💣 Spéciales 💣️", fill="white", font="Helvetica 13")
            joueur.button_attaque_speciale.bind("<Button>", lambda event,joueur=joueur:self.showAttackWindow(event,joueur))

    def hide(self, joueur):

        #print("hide is launched", joueur.couleur)
        bar = joueur.bar
        text = joueur.text_energie
        self.itemconfig(bar, state='hidden')
        self.itemconfig(text, state='hidden')
        joueur.button_attaque_speciale.place_forget()

    def show(self, joueur):
        self.animQueue = []
        #print("show is launched",  joueur.couleur)
        for joueur_x in self.joueurs:
            self.hide(joueur_x)
        bar = joueur.bar
        energy = joueur.joueur_energie
        coords = self.coords(bar)
        total_height = self.bottom - self.top
        required = int(__parametres__.get("red_bull_required"))
        real_height = total_height / required
        test = energy % required
        """
        if energy % required == 0:
            test = required
        """
        to = self.bottom - (real_height * (test))
        self.coords(bar, coords[0], to, coords[2], coords[3])
        text = joueur.text_energie
        button = joueur.button_attaque_speciale
        self.itemconfig(bar, state='normal')
        self.itemconfig(text, state='normal')
        if joueur.attaques_en_banque > 0:
            joueur.button_attaque_speciale.place(x=2, y=self.height+80)
        #print("Done with show")


    def updateBar(self, joueur, **args):
        if "refreshBar" not in args:
            args["refreshBar"] = True
        if "refreshTest" not in args:
            args["refreshTest"] = True
        #print("updating is launched",  joueur.couleur)
        if self.watch_mode:
            self.buttonAnnuler.place_forget()
        if joueur.type_joueur != "Humain":
            return
        bar = joueur.bar
        text = joueur.text_energie
        energy = joueur.joueur_energie
        total_height = self.bottom - self.top
        required = int(__parametres__.get("red_bull_required"))
        real_height = total_height / required
        test = energy % required
        if energy%required == 0:
             test = required
        #self.coords(bar,self.left,self.bottom-(real_height*energy),self.right,self.bottom )
        if args["refreshTest"]:
            self.itemconfig(text, text="⚡ " + str(energy) + " ⚡ ")
        if args["refreshBar"] :
            self.animQueue.append(self.bottom-(real_height*(test)))
            self.barAnimation(bar)
        #print("Joueur a ",joueur.attaques_en_banque, "attaques en banque")
        if joueur.attaques_en_banque > 0:
            joueur.button_attaque_speciale.place(x=2, y=self.height+80)
        else:
            joueur.button_attaque_speciale.place_forget()
        #joueur.bar = self.create_rectangle(left,bottom-(real_height*energy),right,bottom,fill=joueur.couleur)

    def barAnimation(self, bar_id, fromCoor = None):
        """
        try:
            self.after_cancel(self.after_id)
        except:
            pass
        """

        if len(self.animQueue) == 0:
            return
        coords = self.coords(bar_id)
        actuel = coords[1]
        to = self.animQueue[0]
        #print("bar animation", actuel, to)
        state = self.itemcget(bar_id, "state")
        if state == "hidden":
            return

        dif = actuel - to
        if dif > 2:
            if dif > 30:
                actuel = actuel - 10
            if dif > 15:
                actuel = actuel - 8
            else:
                actuel = to
        elif dif < -2:
            if dif < -30:
                actuel = actuel + 10
            if dif < -15:
                actuel = actuel + 8
            else:
                actuel = to
        else:
            actuel = to

        self.coords(bar_id, coords[0], actuel, coords[2], coords[3])

        if actuel != to:
            self.after_id = self.after(100, lambda bar_id=bar_id:self.barAnimation(bar_id, coords[1]))
        else:
            self.animQueue.pop(0)
            if len(self.animQueue) > 0:
                self.barAnimation(bar_id)
        if actuel == self.top:
            if len(self.animQueue) > 0:
                self.animQueue = [self.animQueue[-1]]
            else:
                self.animQueue = [self.bottom]
            self.barAnimation(bar_id)

    def showAttackWindow(self, event, joueur):
        self.dernierJoueur = joueur
        self.dernierButtonAttaque = joueur.button_attaque_speciale
        self.attackWindow = FenetreAttaquesSpeciales(self.parent,joueur)

    def cancelAttack(self, event):
        self.watch_mode = False
        self.buttonAnnuler.place_forget()
        self.dernierButtonAttaque.place(x=2, y=self.height+80)
        self.showAttackWindow(None, self.dernierJoueur)

class FenetreAttaquesSpeciales(Toplevel):

    def __init__(self, parent, joueur):
        super().__init__(parent)
        self.joueur = joueur
        self.parent = parent
        self.canvas = self.parent.canvas_carte
        self.transient(parent)
        self.grab_set()
        self.title("Attaques Spéciales")

        energie = joueur.joueur_energie
        self.base_cost = base_cost = int(__parametres__.get("red_bull_required"))
        self.attaques = {
            "sauter_tour": {
                "nom": "Un ennemi saute\nson tour",
                "description": "Vous pourrez choisir un joueur ennemi\nqui sautera son prochain tour",
                "instructions": "Choissisez un joueur ci-dessous qui sautera sont tour",
                "cost": base_cost,
                "command": self.sauter_tour,
                "image": "attaque_speciale_icons/sauter.png"
            },
            "bomb_voyage" : {
                "nom" : "Exploser une\ncase ennemie",
                "description" : "Vous pourrez faire exploser, faire disparaitre,\nune case d'un ennemi de la carte",
                "instructions": "Choissisez une case ennemie que vous désirez faire exploser!",
                "cost" : base_cost,
                "command" : self.bomb_voyage,
                "image" : "attaque_speciale_icons/explotion.png.png"
            },
            "voler_case" : {
                "nom": "Voler une\ncase ennemie",
                "description": "Vous pourrez sélectionner un case ennemie sur la carte et obtenir\nnon seulement la case, mais les dés sur celle-ci",
                "instructions": "Choissisez une case ennemie que vous désirez voler",
                "cost" : base_cost * 2,
                "command" : self.voler_case,
                "image" : "attaque_speciale_icons/voler_case.png"
            },
            "voler_des": {
                "nom": "Voler des\ndés ennemies",
                "description": "Vous pourrez voler tous les dés moins un d'une case ennemie.\nLes dés volés seront distribuer à la fin de votre tour",
                "instructions": "Choissisez une case ennemie de laquelle vous désirez voler les dés",
                "cost": base_cost * 2,
                "command": self.voler_des,
                "image" : "attaque_speciale_icons/voler_des.png"
            }
        }
        if __parametres__.get("easter_eggs"):
            self.attaques["bomb_voyage"]["nom"] = "Bas de bébé"
            self.attaques["bomb_voyage"]["description"] = "Utiliser un bas de bébé pour\neffacer une case"
            self.attaques["bomb_voyage"]["instructions"] = "Choissisez une case ennemie que vous désirez faire effacer!"
            self.attaques["bomb_voyage"]["image"] = "attaque_speciale_icons/bas.png"
        counter = 0
        label = Label(self, text="Vous avez ⚡️"+str(energie)+"⚡️ disponibles", font="Helvetica 24 bold")
        label.pack()
        for attaque_id, info in self.attaques.items():
            if counter % 2 == 0:
                div = Frame(self)
            photo = Image.open(info["image"])
            photo = photo.resize((40,40))
            photo = ImageTk.PhotoImage(photo)
            button = Button(div, image=photo, compound="top", text=info["nom"]+"\n⚡️"+str(info["cost"])+"⚡️", width=100, height=100, command=lambda id=attaque_id:self.showDescription(id))
            button.image = photo
            if energie < info["cost"]:
                button["state"] = "disabled"
            button.pack(side="left")
            counter += 1
            if counter // 2 == 0:
                div.pack()
        div.pack()

    def showDescription(self, attaque_id):
        w = AttaquesDescription(self, attaque_id)

    def doneAttaque(self):
        self.canvas.attaque_speciale_en_cours = None
        self.canvas.joueur_action_speciale = None
        self.joueur.attaques_en_banque = self.joueur.attaques_en_banque - (self.cost / self.base_cost)
        self.joueur.joueur_energie -= self.cost
        self.parent.energy_bar.updateBar(self.joueur, refreshBar=False)
        self.parent.energy_bar.buttonAnnuler.place_forget()

    def standard(self):
        self.parent.watch_mode = True
        self.parent.energy_bar.dernierButtonAttaque.place_forget()
        self.parent.energy_bar.buttonAnnuler.place(x=2, y=self.parent.energy_bar.height+80)
        self.canvas.attaque_speciale_callback = self.doneAttaque

    def bomb_voyage(self):
        self.cost = self.attaques["bomb_voyage"]["cost"]
        self.canvas.joueur_action_speciale = self.joueur
        self.canvas.attaque_speciale_en_cours = "explotion"
        self.standard()

    def voler_case(self):
        self.cost = self.attaques["voler_case"]["cost"]
        self.canvas.joueur_action_speciale = self.joueur
        self.canvas.attaque_speciale_en_cours = "voler_case"
        self.standard()

    def voler_des(self):
        self.cost = self.attaques["voler_case"]["cost"]
        self.canvas.joueur_action_speciale = self.joueur
        self.canvas.attaque_speciale_en_cours = "voler_des"
        self.standard()

    def sauter_tour(self):
        self.cost = self.attaques["sauter_tour"]["cost"]
        self.standard()
        labels = self.parent.frame_joueur.labels_joueurs
        index = 0
        for label in labels:
            label.bind("<Button>",lambda event,index=index:self.sauter_tour_after(event,index))
            index += 1

    def sauter_tour_after(self, event, index):
        joueur_selection = self.parent.joueurs[index]
        if joueur_selection == self.joueur:
            messagebox.showerror("Erreur","Vous ne pouvez vous sélectionner vous-même")
            return
        confirm = messagebox.askokcancel("Confirmation","Voulez-vous que le joueur '"+str(joueur_selection.couleur)+"' saute son prochain tour?")
        if confirm:
            joueur_selection.sauter_tour = True
            labels = self.parent.frame_joueur.labels_joueurs
            for label in labels:
                label.unbind("<Button>")
            self.doneAttaque()

class AttaquesDescription(Toplevel):

    def __init__(self, parent, id):
        super().__init__(parent)
        self.id = id
        self.parent = parent
        self.transient(parent)
        self.grab_set()
        self.title("Description d'attaque spéciale")
        self.attaque = parent.attaques[id]
        self.header = Label(self, text=self.attaque["nom"], font="Helvetica 18 bold")
        self.header.pack(pady=5, padx=5)
        self.description =Label(self, text=self.attaque["description"])
        self.description.pack(pady=5, padx=5)
        div = Frame(self)
        self.dontDo = Button(div, text="Annuler", command=self.annuler)
        self.dontDo.pack(side="left", pady=5, padx=5)
        self.do = Button(div, text="Utiliser cette attaque", command=self.doAttack)
        self.do.pack(side="left",pady=5, padx=5)
        div.pack()

    def annuler(self):
        self.destroy()

    def doAttack(self):
        self.parent.parent.frame_message.afficher_message(self.attaque["instructions"])
        self.attaque["command"]()
        self.destroy()
        self.parent.destroy()