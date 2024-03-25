"""
Module contenant la classe FenetreAudio. Cette classe permet de gérer la musique
accessible depuis le bouton 🎵 de la fenêtre principale.
"""


from pygame import mixer
from tkinter import Tk, Button, GROOVE, Scale, HORIZONTAL, Label

liste_musics = ["While True.mp3", "We Are The Champions.mp3", "I Will Survive.mp3"]


class FenetreAudio(Tk):
    def __init__(self, x, y):
        """
        Constructeur de la classe FenetreAudio. Permet l'initialisation de la musique
        de fond du jeu.
        """
        super().__init__()
        self.title("Paramètres audio")
        self.geometry(f"+{x+30}+{y-40}")

        # initialisation de la musique
        self.audio_on_and_off = False
        self.compteur = 0
        self.play_and_stop = Button(self, text="▶", relief=GROOVE, command=self.audio_statut)
        self.previous = Button(self, text="<<", relief=GROOVE, command=self.previous_song)
        self.next = Button(self, text=">>", relief=GROOVE, command=self.next_song)
        self.restart = Button(self, text="⟲", relief=GROOVE, command=self.start_audio)
        self.volume = Scale(self, orient=HORIZONTAL, from_=0, to=100, command=self.volume_song)
        self.volume.set(50)
        self.titre = Label(self, text=liste_musics[self.compteur][:-4], width=20, fg="blue")

        self.titre.grid(row=0, columnspan=4)

        self.previous.grid(row=1, column=0, pady=(5, 0), padx=(12, 0))
        self.play_and_stop.grid(row=1, column=1, pady=(5, 0))
        self.next.grid(row=1, column=2, pady=(5, 0))
        self.restart.grid(row=1, column=3, pady=(5, 0), padx=(0, 5))
        self.volume.grid(row=2, columnspan=4, padx=(8, 0))

    def start_audio(self):
        """
        demarrage de la musique
        """
        self.titre["text"] = liste_musics[self.compteur][:-4]
        mixer.music.load(liste_musics[self.compteur])
        mixer.music.play(loops=-1)

    def audio_statut(self):
        """
        Cette méthode modifie le statut de l'audio (ON/OFF)
        """
        if not self.audio_on_and_off:
            mixer.music.unpause()
            self.play_and_stop["text"] = "□"
        if self.audio_on_and_off:
            mixer.music.pause()
            self.play_and_stop["text"] = "▶"
        self.audio_on_and_off = not self.audio_on_and_off

    def previous_song(self):
        """
        Cette méthode permet de revenir à la musique précedente
        """
        self.compteur = (self.compteur - 1) % 3
        self.start_audio()

    def next_song(self):
        """
        Cette méthode permet de revenir à la musique précedente
        """
        self.compteur = (self.compteur + 1) % 3
        self.start_audio()

    def volume_song(self, x):
        """
        Cette méthode permet de modifier le volume de la musique
        Args:
            x (int): Volume de la musique (entre 0 et 100)
        """
        mixer.music.set_volume(self.volume.get())