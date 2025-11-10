import tkinter as tk
import requests
import logging

logger = logging.getLogger(__name__)

class PlayActionScreen(tk.Frame):
    def __init__(self, parent, players_red, players_green, api_url="http://localhost:5000"):
        super().__init__(parent, bg = "black")
        
        # store user entered player names
        self.players_red = players_red
        self.players_green = players_green
        self.api_url = api_url
        
        # Timer variables
        self.time_remaining = 6 * 60  # 6 minutes in seconds
        self.timer_label = None
        
        # Score tracking
        self.score_labels = {}  # equipment_id -> label widget
        self.player_equipment_map = {}  # codename -> equipment_id
        self.last_event_timestamp = 0  # Track last event we've seen

        # divide scoreboard into 2
        self.top_frame = tk.Frame(self, bg = "#1a1a1a", highlightbackground = "white", highlightthickness = 2)
        self.bottom_frame = tk.Frame(self, bg = "#0f0f0f", highlightbackground = "white", highlightthickness = 2)

        self.top_frame.pack(fill = "both", expand = True, padx = 50, pady = (30, 10))
        self.bottom_frame.pack(fill = "both", expand = True, padx = 50, pady = (10, 30))

        self.build_top_half()
        self.build_bottom_half()
        
        # Start with pregame countdown
        self.pregame_countdown()
        # Start polling immediately
        self.poll_game_state()
        self.poll_game_events()

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
            # Store reference to update later
            self.score_labels[name] = score_label

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
            # Store reference to update later
            self.score_labels[name] = score_label

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
            text = "Time Remaining: 06:00",
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
            state = "disabled",  # Start disabled, enable when adding text
            wrap = "word"
        )
        self.action_text.pack(side = "left", expand = True, fill = "both")
        
        # Configure text tags for different event types
        self.action_text.tag_config("friendly_fire", foreground="#FF6B6B", font=("Arial", 14, "bold"))
        self.action_text.tag_config("base_hit", foreground="#4ECDC4", font=("Arial", 14, "bold"))
        self.action_text.tag_config("normal_hit", foreground="white")
        self.action_text.tag_config("timestamp", foreground="#888888", font=("Arial", 12))
    
    def pregame_countdown(self):
        self.pre_time_remaining = 30 # 30 seconds
        self.update_pregame_timer()

    def update_pregame_timer(self):
        if self.pre_time_remaining <= 0:
            self.timer_label.config(text="Time Remaining: 06:00")
            self.time_remaining = 6 * 60
            self.update_game_timer()
            return
        
        minutes = self.pre_time_remaining // 60
        seconds = self.pre_time_remaining % 60
        self.timer_label.config(text=f"Game starts in: {minutes:02d}:{seconds:02d}")

        self.pre_time_remaining -= 1
        self.after(1000, self.update_pregame_timer)

    def update_game_timer(self):
        """Update the countdown timer every second"""
        if self.time_remaining <= 0:
            self.timer_label.config(text="Time Remaining: 00:00", fg="red")
            return

        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        time_update = f"Time Remaining: {minutes:02d}:{seconds:02d}"

        self.timer_label.config(text=time_update)

        self.time_remaining -= 1
        self.after(1000, self.update_game_timer)
    
    def poll_game_state(self):
        """Poll the backend for current game state (scores)"""
        try:
            response = requests.get(f"{self.api_url}/game/state", timeout=1)
            if response.status_code == 200:
                data = response.json()
                self.update_scores(data)
        except Exception as e:
            logger.debug(f"Error polling game state: {e}")
        
        # Poll every 2 seconds
        self.after(2000, self.poll_game_state)
    
    def poll_game_events(self):
        """Poll the backend for new game events"""
        try:
            params = {}
            if self.last_event_timestamp > 0:
                params['since'] = self.last_event_timestamp
            
            response = requests.get(f"{self.api_url}/game/events", params=params, timeout=1)
            if response.status_code == 200:
                data = response.json()
                events = data.get('events', [])
                
                for event in events:
                    self.add_event_to_log(event)
                    # Update last timestamp
                    if event['timestamp'] > self.last_event_timestamp:
                        self.last_event_timestamp = event['timestamp']
                        
        except Exception as e:
            logger.debug(f"Error polling game events: {e}")
        
        # Poll every 1 second for events
        self.after(1000, self.poll_game_events)
    
    def update_scores(self, game_data):
        """Update score labels with current scores"""
        try:
            # Update red team scores
            for player in game_data.get('red_team', {}).get('players', []):
                codename = player['codename']
                score = player['score']
                if codename in self.score_labels:
                    self.score_labels[codename].config(text=str(score))
            
            # Update green team scores
            for player in game_data.get('green_team', {}).get('players', []):
                codename = player['codename']
                score = player['score']
                if codename in self.score_labels:
                    self.score_labels[codename].config(text=str(score))
                    
        except Exception as e:
            logger.error(f"Error updating scores: {e}")
    
    def add_event_to_log(self, event):
        """Add a game event to the action log"""
        try:
            event_type = event.get('type', 'unknown')
            message = event.get('message', '')
            
            # Determine tag based on event type
            if event_type == 'friendly_fire':
                tag = "friendly_fire"
            elif event_type == 'base_hit':
                tag = "base_hit"
            else:
                tag = "normal_hit"
            
            # Enable text widget for editing
            self.action_text.config(state="normal")
            
            # Add the message with appropriate styling
            self.action_text.insert("end", f"• {message}\n", tag)
            
            # Auto-scroll to bottom
            self.action_text.see("end")
            
            # Disable editing again
            self.action_text.config(state="disabled")
            
        except Exception as e:
            logger.error(f"Error adding event to log: {e}")
