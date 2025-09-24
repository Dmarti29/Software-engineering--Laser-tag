import tkinter as tk

class PlayerEntry(tk.Frame):
    def __init__(self, parent):
        # call frames constructor
        tk.Frame.__init__(self, parent)

        # grid layout for each teams side
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)

        # green team side
        self.green_team_side = tk.Frame(self, bg = "green")
        self.green_team_side.grid(row = 0, column = 0, sticky = "nsew")

        tk.Label(self.green_team_side, text = "GREEN TEAM", bg = "green", fg = "white", font = ("Arial", 16, "bold")).pack(pady = 5)

        # slots for user to enter player names into player entry screen, 10 slots per team
        self.green_team_slots = []
        for i in range(10):
            entry = tk.Entry(self.green_team_side, font = ("Arial", 12), justify = "center")
            entry.pack(padx = 10, pady = 2, fill = "x")
            self.green_team_slots.append(entry)