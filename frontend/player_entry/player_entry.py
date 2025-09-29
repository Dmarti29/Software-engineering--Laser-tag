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
        
        # Create player slots with add buttons and ID fields
        self.player_slots = []
        self.player_id_entries = []
        self.player_buttons = []
        
        # Create a container frame for player entries
        entries_frame = tk.Frame(self.frame)
        entries_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create header labels
        header_frame = tk.Frame(entries_frame)
        header_frame.pack(fill="x", pady=2)
        
        name_label = tk.Label(header_frame, text="Player Name", font=("Arial", 10, "bold"))
        name_label.pack(side="left", fill="x", expand=True)
        
        id_label = tk.Label(header_frame, text="Player ID", font=("Arial", 10, "bold"), width=8)
        id_label.pack(side="left", padx=5)
        
        # Empty space for button column
        tk.Label(header_frame, text="", width=5).pack(side="right")
        
        # Create player slots (10 slots per team)
        for i in range(10):
            slot_frame = tk.Frame(entries_frame)
            slot_frame.pack(fill="x", pady=2)
            
            # Create name entry field
            entry = tk.Entry(slot_frame, font=("Arial", 12), justify="center")
            entry.pack(side="left", fill="x", expand=True)
            self.player_slots.append(entry)
            
            # Create ID entry field
            id_entry = tk.Entry(slot_frame, font=("Arial", 12), justify="center", width=8)
            # Default to the auto-generated ID
            default_id = team_id_generator(self.team_name, i)
            id_entry.insert(0, str(default_id))
            id_entry.pack(side="left", padx=5)
            self.player_id_entries.append(id_entry)
            
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
            
    def set_player_id(self, index, player_id):
        """Sets a player ID at the specified index"""
        if 0 <= index < len(self.player_id_entries):
            self.player_id_entries[index].delete(0, tk.END)
            self.player_id_entries[index].insert(0, str(player_id))
    
    def clear_all_entries(self):
        """Clears all player name and ID entries"""
        # Clear player names
        for entry in self.player_slots:
            entry.delete(0, tk.END)
        
        # Reset player IDs to default values
        for i, id_entry in enumerate(self.player_id_entries):
            id_entry.delete(0, tk.END)
            default_id = team_id_generator(self.team_name, i)
            id_entry.insert(0, str(default_id))
    
    def add_player(self, index):
        """Add a player to the backend"""
        codename = self.player_slots[index].get().strip()
        
        if not codename:
            messagebox.showerror("Error", "Please enter a player name")
            return
        
        # Get custom player ID from entry field
        try:
            player_id_text = self.player_id_entries[index].get().strip()
            if not player_id_text:
                # Use default ID if empty
                player_id = team_id_generator(self.team_name, index)
            else:
                player_id = int(player_id_text)
        except ValueError:
            messagebox.showerror("Error", "Player ID must be a number")
            return
        
        # Generate equipment ID based on team
        equipment_id = equipment_id_generator(self.team_name, index)
        
        # Send to backend
        result = self.api_client.add_player(player_id, codename, equipment_id)
        
        if "error" in result:
            messagebox.showerror("Error", f"Failed to add player: {result['error']}")
        else:
            messagebox.showinfo("Success", f"{codename} added to {self.team_name} team with ID {player_id}")
    
    def get_player_ids(self):
        """Returns a list of all player IDs"""
        player_ids = []
        for i, id_entry in enumerate(self.player_id_entries):
            try:
                player_id_text = id_entry.get().strip()
                if player_id_text and self.player_slots[i].get().strip():
                    player_ids.append(int(player_id_text))
            except (ValueError, IndexError):
                continue
        return player_ids
    
    def get_equipment_ids(self):
        """Get equipment IDs for this team"""
        equipment_ids = []
        for i, entry in enumerate(self.player_slots):
            if entry.get().strip():
                equipment_ids.append(equipment_id_generator(self.team_name, i))
        return equipment_ids
