import tkinter as tk
from player_entry.player_entry import PlayerEntry

class RedTeamEntry(PlayerEntry):
    """
    Red Team specific implementation of PlayerEntry.
    This class extends the base PlayerEntry and adds red team specific functionality.
    """
    
    def __init__(self, parent):
        # Initialize base class with red team specifics
        super().__init__(parent, "Red", "red")
    
    # Red team specific endpoints
    def get_red_team_data(self):
        """
        Returns data specific to red team that would be sent to backend
        """
        return {
            "team_name": "Red",
            "players": self.get_player_names()
        }
    
    def sync_with_backend(self, backend_data):
        """
        Syncs player names with data from backend
        """
        if "players" in backend_data and isinstance(backend_data["players"], list):
            for i, name in enumerate(backend_data["players"]):
                if i < len(self.player_slots):
                    self.set_player_name(i, name)
