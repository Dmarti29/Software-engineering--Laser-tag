import tkinter as tk
import requests
import logging

logger = logging.getLogger(__name__)

class PlayActionScreen(tk.Frame):
    def __init__(self, parent, players_red, players_green):
        super().__init__(parent, bg = "black")
        
        # store user entered player names
        self.players_red = players_red
        self.players_green = players_green
        
        # API configuration
        self.api_url = "http://localhost:5000"
        self.poll_interval = 2000  # Poll every 2 seconds
        
        # Timer variables
        self.time_remaining = 300  # 5 minutes in seconds
        self.timer_label = None
        
        # Score tracking dictionaries (codename -> label widget)
        self.red_score_labels = {}
        self.green_score_labels = {}

        # divide scoreboard into 2
        self.top_frame = tk.Frame(self, bg = "#1a1a1a", highlightbackground = "white", highlightthickness = 2)
        self.bottom_frame = tk.Frame(self, bg = "#0f0f0f", highlightbackground = "white", highlightthickness = 2)

        self.top_frame.pack(fill = "both", expand = True, padx = 50, pady = (30, 10))
        self.bottom_frame.pack(fill = "both", expand = True, padx = 50, pady = (10, 30))

        self.build_top_half()
        self.build_bottom_half()
        
        # Start the countdown and polling
        self.update_timer()

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
            score_label = tk.Label(row, text = "0", font = ("Arial", 16, "bold"), fg = "yellow", bg = "#1a1a1a", anchor = "e")
            score_label.pack(side = "right", padx = 10)
            self.red_score_labels[name] = score_label

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
            score_label = tk.Label(row, text = "0", font = ("Arial", 16, "bold"), fg = "yellow", bg = "#1a1a1a", anchor = "e")
            score_label.pack(side = "right", padx = 10)
            self.green_score_labels[name] = score_label

    # GAME ACTION / TIMER (BOTTOM HALF) #
    def build_bottom_half(self):
        title = tk.Label(
            self.bottom_frame, text = "CURRENT GAME ACTION",
            font = ("Arial", 24, "bold"), fg = "white", bg = "#0f0f0f"
        )
        title.pack(pady = 10)

        # Timer
        self.timer_label = tk.Label(
            self.bottom_frame,
            text = "Time Remaining: 05:00",
            font = ("Arial", 18, "bold"),
            fg = "cyan",
            bg = "#0f0f0f"
        )
        self.timer_label.pack(pady = (0, 10))

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
            state = "disabled",  # Disable editing
            wrap = "word"
        )
        self.action_text.pack(side = "left", expand = True, fill = "both")
        
        # Configure tags for colored text
        self.action_text.tag_config("friendly_fire", foreground="#FF6B6B")
        self.action_text.tag_config("hit", foreground="#4ECDC4")
        self.action_text.tag_config("info", foreground="#95E1D3")
        
        # Start polling for game state
        self.poll_game_state()
    
    def update_timer(self):
        """Update the countdown timer every second"""
        if self.time_remaining > 0:
            minutes = self.time_remaining // 60
            seconds = self.time_remaining % 60
            self.timer_label.config(text = f"Time Remaining: {minutes:02d}:{seconds:02d}")
            self.time_remaining -= 1
            self.after(1000, self.update_timer)  # Update every 1000ms (1 second)
        else:
            self.timer_label.config(text = "Time Remaining: 00:00", fg = "red")
    
    def poll_game_state(self):
        """Poll backend for game state updates"""
        try:
            response = requests.get(f"{self.api_url}/game/state", timeout=1)
            if response.status_code == 200:
                data = response.json()
                self.update_scores(data)
                self.update_action_log(data.get('events', []))
        except Exception as e:
            logger.error(f"Error polling game state: {e}")
        
        # Schedule next poll
        self.after(self.poll_interval, self.poll_game_state)
    
    def update_scores(self, data):
        """Update score labels with data from backend"""
        # Update red team scores
        for player in data.get('red_team', {}).get('players', []):
            codename = player.get('codename')
            score = player.get('score', 0)
            if codename in self.red_score_labels:
                self.red_score_labels[codename].config(text=str(score))
        
        # Update green team scores
        for player in data.get('green_team', {}).get('players', []):
            codename = player.get('codename')
            score = player.get('score', 0)
            if codename in self.green_score_labels:
                self.green_score_labels[codename].config(text=str(score))
    
    def update_action_log(self, events):
        """Update action log with recent events"""
        self.action_text.config(state="normal")
        self.action_text.delete(1.0, tk.END)
        
        # Display events in reverse order (newest first)
        for event in reversed(events):
            timestamp = event.get('timestamp', '')
            message = event.get('message', '')
            event_type = event.get('type', 'info')
            
            self.action_text.insert(tk.END, f"[{timestamp}] ", "info")
            self.action_text.insert(tk.END, f"{message}\n", event_type)
        
        self.action_text.config(state="disabled")