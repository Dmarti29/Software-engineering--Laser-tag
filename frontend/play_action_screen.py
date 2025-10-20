import tkinter as tk

class PlayActionScreen(tk.Frame):
    def __init__(self, parent, players_red, players_green):
        super().__init__(parent, bg = "black")
        
        # store user entered player names
        self.players_red = players_red
        self.players_green = players_green

        # divide scoreboard into 2
        self.top_frame = tk.Frame(self, bg = "#1a1a1a", highlightbackground = "white", highlightthickness = 2)
        self.bottom_frame = tk.Frame(self, bg = "#0f0f0f", highlightbackground = "white", highlightthickness = 2)

        self.top_frame.pack(fill = "both", expand = True, padx = 50, pady = (30, 10))
        self.bottom_frame.pack(fill = "both", expand = True, padx = 50, pady = (10, 30))

        self.build_top_half()
        self.build_bottom_half()

    # CURRENT SCORES (TOP HALF) #
    def build_top_half(self):
        title = tk.Label(
            self.top_frame,
            text = "CURRENT SCORES",
            font = ("Arial", 24, "bold"),
            fg = "white",
            bg = "#1a1a1a"
        )
        title.pack(pady = 10)

        # 2 columns for red and green teams
        teams_frame = tk.Frame(self.top_frame, bg = "#1a1a1a")
        teams_frame.pack(expand = True, fill = "both", pady = 10)

        # red team
        red_frame = tk.Frame(teams_frame, bg = "#1a1a1a")
        red_frame.pack(side = "left", expand = True, fill = "both", padx = 20)

        tk.Label(red_frame, text = "RED TEAM", font = ("Arial", 20, "bold"), fg = "red", bg = "#1a1a1a").pack()
        for name in self.players_red:
            if not name.strip():
                continue
            row = tk.Frame(red_frame, bg = "#1a1a1a")
            row.pack(fill = "x", pady = 5)
            tk.Label(row, text = name, font = ("Arial", 16), fg = "white", bg = "#1a1a1a", anchor = "e").pack(side = "left", padx = 10)
            tk.Label(row, text = "0", font = ("Arial", 16, "bold"), fg = "yellow", bg = "#1a1a1a", anchor = "e").pack(side = "right", padx = 10)

        # green team
        green_frame = tk.Frame(teams_frame, bg = "#1a1a1a")
        green_frame.pack(side = "right", expand = True, fill = "both", padx = 20)

        tk.Label(green_frame, text = "GREEN TEAM", font = ("Arial", 20, "bold"), fg = "lime", bg = "#1a1a1a").pack()
        for name in self.players_green:
            if not name.strip():
                continue
            row = tk.Frame(green_frame, bg = "#1a1a1a")
            row.pack(fill = "x", pady = 5)
            tk.Label(row, text = name, font = ("Arial", 16), fg = "white", bg = "#1a1a1a", anchor = "w").pack(side = "left", padx = 10)
            tk.Label(row, text = "0", font = ("Arial", 16, "bold"), fg = "yellow", bg = "#1a1a1a", anchor = "e").pack(side = "right", padx = 10)

    # GAME ACTION / TIMER (BOTTOM HALF) #
    def build_bottom_half(self):
        title = tk.Label(
            self.bottom_frame, text = "CURRENT GAME ACTION",
            font = ("Arial", 24, "bold"), fg = "white", bg = "#0f0f0f"
        )
        title.pack(pady = 10)

        # Timer
        timer_label = tk.Label(
            self.bottom_frame,
            text = "Time Remaining: 05:00",
            font = ("Arial", 18, "bold"),
            fg = "cyan",
            bg = "#0f0f0f"
        )
        timer_label.pack(pady = (0, 10))

        # Action log
        action_frame = tk.Frame(self.bottom_frame, bg = "#0f0f0f")
        action_frame.pack(expand = True, fill = "both", padx = 30, pady = 10)

        self.action_text = tk.Text(
            action_frame,
            height = 6,
            font = ("Arial", 14),
            fg = "white",
            bg = "#0f0f0f",
            relief = "flat",
            state = "normal",
            wrap = "word"
        )
        self.action_text.pack(side = "left", expand = True, fill = "both")