import tkinter as tk
import requests
import logging
from PIL import Image, ImageTk

logger = logging.getLogger(__name__)

class PlayActionScreen(tk.Frame):
    def __init__(self, parent, players_red, players_green, api_url="http://localhost:5000", return_callback=None):
        super().__init__(parent, bg = "black")
        
        # Store callback for returning to player entry
        self.return_callback = return_callback
        
        # store user entered player names
        self.players_red = players_red
        self.players_green = players_green
        self.api_url = api_url
        
        # Timer variables
        self.time_remaining = 6 * 60  # 6 minutes in seconds
        self.timer_label = None
        
        # Score tracking
        self.score_labels = {}  # codename -> label widget
        self.player_equipment_map = {}  # codename -> equipment_id
        self.last_event_timestamp = 0  # Track last event we've seen
        
        # Team total labels
        self.red_team_total_label = None
        self.green_team_total_label = None
        
        # Frames to hold dynamic player lists
        self.red_players_frame = None
        self.green_players_frame = None
        
        # Flash state for winning team
        self.flash_state = False
        self.start_flashing()

        # divide scoreboard into 2
        self.top_frame = tk.Frame(self, bg = "#1a1a1a", highlightbackground = "white", highlightthickness = 2)
        self.bottom_frame = tk.Frame(self, bg = "#0f0f0f", highlightbackground = "white", highlightthickness = 2)

        self.top_frame.pack(fill = "both", expand = True, padx = 50, pady = (30, 10))
        self.bottom_frame.pack(fill = "both", expand = True, padx = 50, pady = (10, 30))

        self.build_top_half()
        self.build_bottom_half()
        
        # Start game timer immediately (pregame countdown already happened)
        self.update_game_timer()
        # Start polling immediately
        self.poll_game_state()
        self.poll_game_events()

        # load base icon
        try:
            base_img = Image.open("frontend/assets/baseicon.jpg")
            base_img = base_img.resize((20, 20), Image.Resampling.LANCZOS)  # Resize to 20x20 pixels
            self.base_icon = ImageTk.PhotoImage(base_img)
        except Exception as e:
            logger.error(f"Failed to load base icon: {e}")
            self.base_icon = None

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

        # Red team header with total
        red_header_frame = tk.Frame(red_frame, bg = "#1a1a1a")
        red_header_frame.pack(fill = "x", pady = 5)
        tk.Label(red_header_frame, text = "RED TEAM", font = ("Arial", 20, "bold"), fg = "red", bg = "#1a1a1a").pack(side = "left")
        self.red_team_total_label = tk.Label(red_header_frame, text = "Total: 0", font = ("Arial", 18, "bold"), fg = "#FFD700", bg = "#1a1a1a")
        self.red_team_total_label.pack(side = "right", padx = 10)
        
        # Container for red team players (dynamically rebuilt)
        self.red_players_frame = tk.Frame(red_frame, bg = "#1a1a1a")
        self.red_players_frame.pack(fill = "both", expand = True)

        # green team
        green_frame = tk.Frame(teams_frame, bg = "#1a1a1a")
        green_frame.pack(side = "right", expand = True, fill = "both", padx = 20)

        # Green team header with total
        green_header_frame = tk.Frame(green_frame, bg = "#1a1a1a")
        green_header_frame.pack(fill = "x", pady = 5)
        tk.Label(green_header_frame, text = "GREEN TEAM", font = ("Arial", 20, "bold"), fg = "lime", bg = "#1a1a1a").pack(side = "left")
        self.green_team_total_label = tk.Label(green_header_frame, text = "Total: 0", font = ("Arial", 18, "bold"), fg = "#FFD700", bg = "#1a1a1a")
        self.green_team_total_label.pack(side = "right", padx = 10)
        
        # Container for green team players (dynamically rebuilt)
        self.green_players_frame = tk.Frame(green_frame, bg = "#1a1a1a")
        self.green_players_frame.pack(fill = "both", expand = True)

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
        
        # Add Return to Player Entry button
        if self.return_callback:
            button_frame = tk.Frame(self.bottom_frame, bg = "#0f0f0f")
            button_frame.pack(pady = 10)
            
            return_button = tk.Button(
                button_frame,
                text = "Return to Player Entry",
                font = ("Arial", 14, "bold"),
                fg = "white",
                bg = "#FF6B6B",
                activebackground = "#FF5252",
                activeforeground = "white",
                relief = "raised",
                bd = 3,
                padx = 20,
                pady = 10,
                command = self.return_to_player_entry
            )
            return_button.pack()
    
    def return_to_player_entry(self):
        """Handle returning to player entry screen"""
        try:
            # Stop any ongoing timers
            self.after_cancel(self.update_game_timer)
        except:
            pass
        
        # Call the return callback if provided
        if self.return_callback:
            self.return_callback()
    

    def update_game_timer(self):
        """Update the countdown timer every second"""
        if self.time_remaining <= 0:
            self.timer_label.config(text="Time Remaining: 00:00", fg="red")
            
            # Call backend to end game (broadcasts code 221 three times)
            try:
                requests.post(f"{self.api_url}/game/end", timeout=2)
                logger.info("Game ended - code 221 broadcasted 3 times")
            except Exception as e:
                logger.error(f"Failed to end game: {e}")
            
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
    
    def start_flashing(self):
        """Toggle flash state every 500ms for winning team effect"""
        self.flash_state = not self.flash_state
        self.after(500, self.start_flashing)
    
    def update_scores(self, game_data):
        """Update score labels with current scores (sorted by score, with team totals)"""
        try:
            # Update red team
            red_team_data = game_data.get('red_team', {})
            red_players = red_team_data.get('players', [])
            red_total = red_team_data.get('total_score', 0)
            
            # Update green team data
            green_team_data = game_data.get('green_team', {})
            green_players = green_team_data.get('players', [])
            green_total = green_team_data.get('total_score', 0)
            
            # Determine winning team
            red_winning = red_total > green_total
            green_winning = green_total > red_total
            
            # Update red team total with flashing if winning
            if self.red_team_total_label:
                if red_winning and self.flash_state:
                    self.red_team_total_label.config(text=f"Total: {red_total}", fg="#FF0000")  # Bright red
                elif red_winning:
                    self.red_team_total_label.config(text=f"Total: {red_total}", fg="#FFD700")  # Gold
                else:
                    self.red_team_total_label.config(text=f"Total: {red_total}", fg="#FFD700")  # Gold (not winning)
            
            # Rebuild red team player list (already sorted highest to lowest by backend)
            for widget in self.red_players_frame.winfo_children():
                widget.destroy()
            
            for player in red_players:
                codename = player['codename']
                score = player['score']
                hit_base = player.get('hit_base', False)
                
                row = tk.Frame(self.red_players_frame, bg = "#1a1a1a")
                row.pack(fill = "x", pady = 3)
                
                # show base icon after a player hits the base
                if hit_base and self.base_icon:
                    icon_label = tk.Label(row, image = self.base_icon, bg = "#1a1a1a")
                    icon_label.pack(side = "left", padx = (10, 5))

                tk.Label(row, text = codename, font = ("Arial", 16), fg = "white", bg = "#1a1a1a", anchor = "e").pack(side = "left", padx = 10)
                tk.Label(row, text = str(score), font = ("Arial", 16, "bold"), fg = "yellow", bg = "#1a1a1a", anchor = "e").pack(side = "right", padx = 10)
            
            # Update green team total with flashing if winning
            if self.green_team_total_label:
                if green_winning and self.flash_state:
                    self.green_team_total_label.config(text=f"Total: {green_total}", fg="#00FF00")  # Bright green
                elif green_winning:
                    self.green_team_total_label.config(text=f"Total: {green_total}", fg="#FFD700")  # Gold
                else:
                    self.green_team_total_label.config(text=f"Total: {green_total}", fg="#FFD700")  # Gold (not winning)
            
            # Rebuild green team player list (already sorted highest to lowest by backend)
            for widget in self.green_players_frame.winfo_children():
                widget.destroy()
            
            for player in green_players:
                codename = player['codename']
                score = player['score']
                hit_base = player.get('hit_base', False)
                
                row = tk.Frame(self.green_players_frame, bg = "#1a1a1a")
                row.pack(fill = "x", pady = 3)

                # show base icon after a player hits the base
                if hit_base and self.base_icon:
                    icon_label = tk.Label(row, image = self.base_icon, bg = "#1a1a1a")
                    icon_label.pack(side = "left", padx = (10, 5))
                
                tk.Label(row, text = codename, font = ("Arial", 16), fg = "white", bg = "#1a1a1a", anchor = "w").pack(side = "left", padx = 10)
                tk.Label(row, text = str(score), font = ("Arial", 16, "bold"), fg = "yellow", bg = "#1a1a1a", anchor = "e").pack(side = "right", padx = 10)
                    
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
