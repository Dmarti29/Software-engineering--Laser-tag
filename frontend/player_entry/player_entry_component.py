import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time

from frontend.player_entry.player_teams.red_team_entry import RedTeamEntry
from frontend.player_entry.player_teams.green_team_entry import GreenTeamEntry
from frontend.player_entry.game_status.start_game import StartGameButton
from frontend.player_entry.game_status.end_game import EndGameButton
from frontend.api import ApiClient, transform_players_for_ui

class PlayerEntryComponent(tk.Frame):
    """
    Component that combines both Red and Green team UIs side by side.
    This acts as the main player entry screen.
    """
    
    def __init__(self, parent):
        # Initialize the frame
        tk.Frame.__init__(self, parent)
        
        # Initialize API client
        self.api_client = ApiClient()
        
        # Configure grid layout for side-by-side teams
        self.columnconfigure(0, weight=1)  # Red team column
        self.columnconfigure(1, weight=1)  # Green team column
        self.rowconfigure(0, weight=0)  # Status row
        self.rowconfigure(1, weight=1)  # Team Row
        self.rowconfigure(2, weight=0)  # Network settings row
        self.rowconfigure(3, weight=0)  # Button Row
        
        # Status bar
        self.status_frame = tk.Frame(self)
        self.status_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        self.status_label = tk.Label(self.status_frame, text="Status: Connecting to server...")
        self.status_label.pack(side="left")
        
        self.clear_all_button = tk.Button(self.status_frame, text="Clear All Players", command=self.clear_all_players_backend)
        self.clear_all_button.pack(side="right", padx=10)
        
        # Create team instances
        self.red_team = RedTeamEntry(self)
        self.green_team = GreenTeamEntry(self)
        
        # Position team frames in the grid
        self.red_team.get_frame().grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.green_team.get_frame().grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # Network settings frame
        network_frame = tk.LabelFrame(self, text="Network Settings")
        network_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        tk.Label(network_frame, text="Broadcast Address:").grid(row=0, column=0, padx=5, pady=5)
        self.network_address = tk.StringVar(value="127.0.0.1")
        self.address_entry = tk.Entry(network_frame, textvariable=self.network_address)
        self.address_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.update_network_btn = tk.Button(network_frame, text="Update Network", command=self.update_network_address)
        self.update_network_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Button frame
        button_frame = tk.Frame(self)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        # Inject Start/Stop Game buttons
        self.start_button = StartGameButton(button_frame, command=self.start_game)
        self.start_button.pack(side="left", padx=20)

        stop_button = EndGameButton(button_frame, command=self.stop_game)
        stop_button.pack(side="left", padx=20)
        
        # Start the health check thread
        self.health_thread = threading.Thread(target=self.health_check_loop, daemon=True)
        self.health_thread.start()
    
    def start_game(self):
        """Start the game via backend API"""
        result = self.api_client.start_game()
        if "error" in result:
            messagebox.showerror("Error", f"Failed to start game: {result['error']}")
        else:
            messagebox.showinfo("Success", "Game started successfully")
    
    def stop_game(self):
        """Stop the game via backend API"""
        result = self.api_client.end_game()
        if "error" in result:
            messagebox.showerror("Error", f"Failed to stop game: {result['error']}")
        else:
            messagebox.showinfo("Success", "Game stopped successfully")

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
        
    # Backend communication methods
    
    def refresh_players(self):
        """Fetch and display all players from backend"""
        result = self.api_client.get_all_players()
        if "error" in result:
            self.update_status(f"Error: {result['error']}", "red")
        else:
            # Transform backend data to UI format
            ui_data = transform_players_for_ui(result)
            self.sync_with_backend(ui_data)
            
            count = result.get("count", 0)
            self.update_status(f"Connected to server. {count} players loaded.")
    
    def clear_all_players_backend(self):
        """Clear all players from the backend database"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all players?\nThis will remove them from the database."):
            result = self.api_client.clear_all_players()
            if "error" in result:
                messagebox.showerror("Error", f"Failed to clear players: {result['error']}")
            else:
                messagebox.showinfo("Success", "All players cleared successfully")
                self.clear_all_entries()
    
    def update_network_address(self):
        """Update the network broadcast address"""
        address = self.network_address.get().strip()
        if not address:
            messagebox.showerror("Error", "Please enter a valid network address")
            return
        
        result = self.api_client.set_network_address(address)
        if "error" in result:
            messagebox.showerror("Error", f"Failed to update network address: {result['error']}")
        else:
            messagebox.showinfo("Success", f"Network address updated to {address}")
    
    def update_status(self, message, color="black"):
        """Update status bar with message"""
        self.status_label.config(text=message, fg=color)
    
    def health_check_loop(self):
        """Periodic health check of the backend"""
        while True:
            try:
                result = self.api_client.check_health()
                if "error" in result:
                    self.update_status("Server disconnected", "red")
                else:
                    status = result.get("status", "unknown")
                    if status == "healthy":
                        self.update_status("Connected to server")
                    else:
                        self.update_status(f"Server status: {status}", "orange")
                
                # Also update network settings
                network_result = self.api_client.get_network_settings()
                if "error" not in network_result and "address" in network_result:
                    self.network_address.set(network_result["address"])
                    
            except Exception as e:
                self.update_status(f"Error: {str(e)}", "red")
            
            # Sleep for a few seconds
            time.sleep(10)
