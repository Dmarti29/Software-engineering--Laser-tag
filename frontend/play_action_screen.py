import tkinter as tk

class PlayActionScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Play Action Screen").pack()
        tk.Label(self, text="Team info here").pack()