import tkinter as tk

class PlayerEntry:
    """
    Base class for player entry functionality.
    This class provides the core functionality for managing player entries.
    """
    
    def __init__(self, parent, team_name, team_color):
        # Create the frame for this team
        self.frame = tk.Frame(parent, bg=team_color)
        
        # Set team properties
        self.team_name = team_name
        self.team_color = team_color
        
        # Create label for team name
        tk.Label(self.frame, 
                text=f"{team_name.upper()} TEAM", 
                bg=team_color, 
                fg="white", 
                font=("Arial", 16, "bold")).pack(pady=5)
        
        # Create player slots (10 slots per team)
        self.player_slots = []
        for i in range(10):
            entry = tk.Entry(self.frame, font=("Arial", 12), justify="center")
            entry.pack(padx=10, pady=2, fill="x")
            self.player_slots.append(entry)
    
    def get_frame(self):
        """Returns the frame containing this team's UI"""
        return self.frame
    
    def get_player_names(self):
        """Returns a list of all player names"""
        return [entry.get() for entry in self.player_slots]
    
    def set_player_name(self, index, name):
        """Sets a player name at the specified index"""
        if 0 <= index < len(self.player_slots):
            self.player_slots[index].delete(0, tk.END)
            self.player_slots[index].insert(0, name)
    
    def clear_all_entries(self):
        """Clears all player name entries"""
        for entry in self.player_slots:
            entry.delete(0, tk.END)
