import tkinter as tk
from frontend.player_entry.player_entry import PlayerEntry

class GreenTeamEntry(PlayerEntry):
    """
    Green Team specific implementation of PlayerEntry.
    This class extends the base PlayerEntry and adds green team specific functionality.
    """
    
    def __init__(self, parent):
        # Initialize base class with green team specifics
        super().__init__(parent, "Green", "green")
    
    # Green team specific endpoints
    def get_green_team_data(self):
        """
        Returns data specific to green team that would be sent to backend
        """
        return {
            "team_name": "Green",
            "players": self.get_player_names(),
            "player_ids": self.get_player_ids()
        }
    
    def sync_with_backend(self, backend_data):
        """
        Syncs player names and IDs with data from backend
        """
        # Sync player names
        if "players" in backend_data and isinstance(backend_data["players"], list):
            for i, name in enumerate(backend_data["players"]):
                if i < len(self.player_slots):
                    self.set_player_name(i, name)
        
        # Sync player IDs
        if "player_ids" in backend_data and isinstance(backend_data["player_ids"], list):
            for i, player_id in enumerate(backend_data["player_ids"]):
                if i < len(self.player_id_entries):
                    self.set_player_id(i, player_id)
