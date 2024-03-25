from tkinter import *

class JacobWindow(Toplevel):
    def __init__(self, parent, dic):
        super().__init__(parent)
        for coor, prob in dic.items():
            label = Label(self, text=f"Case {coor} --- Proba : {prob}")
            label.pack()
            self.after(5000, self.destroy)