import tkinter as tk

class EndGameButton(tk.Button):
    def __init__(self, parent, command=None):
        super().__init__(parent, text="Stop Game", command=command or self.default_action)

    # Filler content for what this button will do
    def default_action(self):
        print("Stop Game clicked!")