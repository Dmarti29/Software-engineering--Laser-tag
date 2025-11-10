import tkinter as tk
from tkinter import messagebox, simpledialog
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
        
        # Instructions label
        instruction_label = tk.Label(header_frame, text="Enter Player ID first to lookup or create player", 
                                   font=("Arial", 9, "italic"), fg="gray")
        instruction_label.pack(fill="x", pady=(0, 5))
        
        # Column headers
        columns_frame = tk.Frame(header_frame)
        columns_frame.pack(fill="x")
        
        id_label = tk.Label(columns_frame, text="Player ID (Required)", font=("Arial", 10, "bold"), width=15)
        id_label.pack(side="left", padx=5)
        
        name_label = tk.Label(columns_frame, text="Player Name (Auto-filled or Enter New)", font=("Arial", 10, "bold"))
        name_label.pack(side="left", fill="x", expand=True, padx=5)
        
        # Empty space for button column
        tk.Label(columns_frame, text="", width=8).pack(side="right")
        
        # Create player slots (10 slots per team)
        for i in range(10):
            slot_frame = tk.Frame(entries_frame)
            slot_frame.pack(fill="x", pady=2)
            
            # Create ID entry field (first, as it's required)
            id_entry = tk.Entry(slot_frame, font=("Arial", 12), justify="center", width=15)
            id_entry.pack(side="left", padx=5)
            self.player_id_entries.append(id_entry)
            
            # Create name entry field
            entry = tk.Entry(slot_frame, font=("Arial", 12), justify="center")
            entry.pack(side="left", fill="x", expand=True, padx=5)
            self.player_slots.append(entry)
            
            # Create lookup/add button
            button = tk.Button(slot_frame, text="Lookup/Add", 
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
        
        # Clear player IDs (no default values)
        for id_entry in self.player_id_entries:
            id_entry.delete(0, tk.END)
    
    def add_player(self, index):
        """Add a player to the backend.

        New logic: read the player ID first, try to retrieve the codename from the backend.
        - If a codename exists for that ID, populate the name field and notify the user (do not create).
        - If the player does not exist, require the user to enter a codename and then add the player.
        - After adding, prompt for Hardware ID for UDP broadcasting.
        """
        # Get player ID from entry field (required)
        try:
            player_id_text = self.player_id_entries[index].get().strip()
            if not player_id_text:
                messagebox.showerror("Error", "Player ID is required. Please enter a Player ID first.")
                return
            player_id = int(player_id_text)
        except ValueError:
            messagebox.showerror("Error", "Player ID must be a valid number")
            return

        # First, try to fetch existing player by ID from backend
        fetch_result = self.api_client.get_player(player_id)
        if "error" not in fetch_result and "codename" in fetch_result:
            # Player exists in DB: populate the UI and inform the user
            existing_codename = fetch_result.get("codename", "")
            self.set_player_name(index, existing_codename)
            messagebox.showinfo("Player Exists", f"Player ID {player_id} already exists as '{existing_codename}'.")
            
            # Prompt for Hardware ID for existing player
            hardware_id = simpledialog.askinteger(
                "Hardware ID",
                f"Enter Hardware ID for {existing_codename}:",
                parent=self.frame,
                minvalue=1
            )
            
            if hardware_id:
                # Broadcast the hardware ID via UDP with team assignment
                result = self.api_client.add_player(player_id, existing_codename, hardware_id, team=self.team_name.lower())
                if "error" not in result:
                    messagebox.showinfo("Success", f"Hardware ID {hardware_id} assigned and broadcasted for {existing_codename}")
            return
        else:
            # If the error explicitly says player not found, allow creating a new player
            err = fetch_result.get("error", "")
            if err and "not found" not in err.lower() and err != "":
                # Some other error occurred when fetching
                messagebox.showerror("Error", f"Failed to fetch player: {err}")
                return

        # If we reach here, the player was not found (or backend indicated not found)
        codename = self.player_slots[index].get().strip()
        if not codename:
            messagebox.showerror("Error", "Player not found in database. Please enter a player name to add a new player.")
            return

        # Prompt for Hardware ID instead of auto-generating
        hardware_id = simpledialog.askinteger(
            "Hardware ID",
            f"Enter Hardware ID for {codename}:",
            parent=self.frame,
            minvalue=1
        )
        
        if not hardware_id:
            messagebox.showerror("Error", "Hardware ID is required to add a player.")
            return

        # Send to backend to create new player with user-provided hardware ID and team
        result = self.api_client.add_player(player_id, codename, hardware_id, team=self.team_name.lower())

        if "error" in result:
            messagebox.showerror("Error", f"Failed to add player: {result['error']}")
        else:
            messagebox.showinfo("Success", f"{codename} added to {self.team_name} team with ID {player_id} and Hardware ID {hardware_id}")
    
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
