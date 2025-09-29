import tkinter as tk
from tkinter import messagebox
from frontend.api import ApiClient, team_id_generator, equipment_id_generator

class PlayerEntry:
    """
    Base class for player entry functionality.
    This class provides the core functionality for managing player entries.
    """
    
    # Create a shared API client instance
    api_client = ApiClient()
    
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
        
        # Create player slots with add buttons
        self.player_slots = []
        self.player_buttons = []
        
        # Create a container frame for player entries
        entries_frame = tk.Frame(self.frame)
        entries_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create player slots (10 slots per team)
        for i in range(10):
            slot_frame = tk.Frame(entries_frame)
            slot_frame.pack(fill="x", pady=2)
            
            # Create entry field
            entry = tk.Entry(slot_frame, font=("Arial", 12), justify="center")
            entry.pack(side="left", fill="x", expand=True)
            self.player_slots.append(entry)
            
            # Create add button
            button = tk.Button(slot_frame, text="Add", 
                             command=lambda idx=i: self.add_player(idx))
            button.pack(side="right", padx=5)
            self.player_buttons.append(button)
        
        # Create clear button for the team
        clear_btn = tk.Button(self.frame, text=f"Clear {team_name} Team", 
                            command=self.clear_all_entries)
        clear_btn.pack(pady=10)
    
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
    
    def add_player(self, index):
        """Add a player to the backend"""
        codename = self.player_slots[index].get().strip()
        
        if not codename:
            messagebox.showerror("Error", "Please enter a player name")
            return
        
        # Generate player ID based on team (even for Red, odd for Green)
        player_id = team_id_generator(self.team_name, index)
        
        # Generate equipment ID based on team
        equipment_id = equipment_id_generator(self.team_name, index)
        
        # Send to backend
        result = self.api_client.add_player(player_id, codename, equipment_id)
        
        if "error" in result:
            messagebox.showerror("Error", f"Failed to add player: {result['error']}")
        else:
            messagebox.showinfo("Success", f"{codename} added to {self.team_name} team")
    
    def get_equipment_ids(self):
        """Get equipment IDs for this team"""
        equipment_ids = []
        for i, entry in enumerate(self.player_slots):
            if entry.get().strip():
                equipment_ids.append(equipment_id_generator(self.team_name, i))
        return equipment_ids
