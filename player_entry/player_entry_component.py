import tkinter as tk
from player_entry.player_teams.red_team_entry import RedTeamEntry
from player_entry.player_teams.green_team_entry import GreenTeamEntry

class PlayerEntryComponent(tk.Frame):
    """
    Component that combines both Red and Green team UIs side by side.
    This acts as the main player entry screen.
    """
    
    def __init__(self, parent):
        # Initialize the frame
        tk.Frame.__init__(self, parent)
        
        # Configure grid layout for side-by-side teams
        self.columnconfigure(0, weight=1)  # Red team column
        self.columnconfigure(1, weight=1)  # Green team column
        
        # Create team instances
        self.red_team = RedTeamEntry(self)
        self.green_team = GreenTeamEntry(self)
        
        # Position team frames in the grid
        self.red_team.get_frame().grid(row=0, column=0, sticky="nsew")
        self.green_team.get_frame().grid(row=0, column=1, sticky="nsew")
    
    # Combined data access methods
    def get_all_players(self):
        """
        Returns all player data from both teams
        """
        return {
            "red_team": self.red_team.get_player_names(),
            "green_team": self.green_team.get_player_names()
        }
    
    def get_red_team_data(self):
        """
        Returns red team data
        """
        return self.red_team.get_red_team_data()
    
    def get_green_team_data(self):
        """
        Returns green team data
        """
        return self.green_team.get_green_team_data()
    
    def sync_with_backend(self, backend_data):
        """
        Syncs all player data with backend
        """
        if "red_team" in backend_data:
            self.red_team.sync_with_backend(backend_data["red_team"])
        if "green_team" in backend_data:
            self.green_team.sync_with_backend(backend_data["green_team"])
            
    def clear_all_entries(self):
        """
        Clears all player entries on both teams
        """
        self.red_team.clear_all_entries()
        self.green_team.clear_all_entries()
