import requests
import json
import logging
from typing import Dict, List, Any, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ApiClient:
    """
    Client for communicating with the backend API.
    Handles all HTTP requests to the backend server.
    """
    
    def __init__(self, base_url="http://localhost:5000"):
        """
        Initialize the API client with the base URL of the backend server.
        
        Args:
            base_url (str): Base URL of the backend server
        """
        self.base_url = base_url
        self.session = requests.Session()
    
    def _handle_response(self, response):
        """
        Handle API response and error cases.
        
        Args:
            response: Response from requests
            
        Returns:
            dict: Response data or error message
        """
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            try:
                return {"error": response.json().get("error", str(e))}
            except:
                return {"error": str(e)}
        except requests.exceptions.ConnectionError:
            logger.error("Connection error: Could not connect to server")
            return {"error": "Could not connect to server"}
        except requests.exceptions.Timeout:
            logger.error("Timeout error: Server took too long to respond")
            return {"error": "Server took too long to respond"}
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON response: {response.text}")
            return {"error": "Invalid response from server"}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {"error": f"Unexpected error: {str(e)}"}
    
    # Player Management Endpoints
    
    def get_all_players(self) -> Dict:
        """
        Get all players from the backend.
        
        Returns:
            dict: Players data with structure:
            {
                "players": [{"id": 1, "codename": "Player1"}, ...],
                "count": 2
            }
        """
        try:
            response = self.session.get(f"{self.base_url}/players")
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Failed to get players: {e}")
            return {"error": str(e), "players": [], "count": 0}
    
    def add_player(self, player_id: int, codename: str, equipment_id: Optional[int] = None, team: str = "red") -> Dict:
        """
        Add a new player to the backend.
        
        Args:
            player_id (int): ID of the player
            codename (str): Name of the player
            equipment_id (int, optional): Equipment ID for broadcasting
            team (str): Team name - "red" or "green"
            
        Returns:
            dict: Response data with player information
        """
        data = {
            "id": player_id,
            "codename": codename,
            "team": team.lower()
        }
        
        if equipment_id is not None:
            data["equipment_id"] = equipment_id
            
        try:
            response = self.session.post(
                f"{self.base_url}/players", 
                json=data
            )
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Failed to add player: {e}")
            return {"error": str(e)}
    
    def get_player(self, player_id: int) -> Dict:
        """
        Get a player by ID from the backend.
        
        Args:
            player_id (int): ID of the player to retrieve
            
        Returns:
            dict: Player data
        """
        try:
            response = self.session.get(f"{self.base_url}/players/{player_id}")
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Failed to get player {player_id}: {e}")
            return {"error": str(e)}
    
    def clear_all_players(self) -> Dict:
        """
        Clear all players from the backend.
        
        Returns:
            dict: Response message
        """
        try:
            response = self.session.delete(f"{self.base_url}/players")
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Failed to clear players: {e}")
            return {"error": str(e)}
    
    # Network Configuration Endpoints
    
    def get_network_settings(self) -> Dict:
        """
        Get current network settings from the backend.
        
        Returns:
            dict: Network settings data
        """
        try:
            response = self.session.get(f"{self.base_url}/network")
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Failed to get network settings: {e}")
            return {"error": str(e)}
    
    def set_network_address(self, address: str) -> Dict:
        """
        Set network address for UDP broadcasting.
        
        Args:
            address (str): New broadcast address
            
        Returns:
            dict: Response message
        """
        try:
            response = self.session.post(
                f"{self.base_url}/network", 
                json={"address": address}
            )
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Failed to set network address: {e}")
            return {"error": str(e)}
    
    # Game Control Endpoints
    
    def start_game(self) -> Dict:
        """
        Start the game by sending request to backend.
        
        Returns:
            dict: Response message
        """
        try:
            response = self.session.post(f"{self.base_url}/game/start")
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Failed to start game: {e}")
            return {"error": str(e)}
    
    def end_game(self) -> Dict:
        """
        End the game by sending request to backend.
        
        Returns:
            dict: Response message
        """
        try:
            response = self.session.post(f"{self.base_url}/game/end")
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Failed to end game: {e}")
            return {"error": str(e)}
    
    def broadcast_equipment_id(self, equipment_id: int) -> Dict:
        """
        Broadcast equipment ID via UDP.
        
        Args:
            equipment_id (int): Equipment ID to broadcast
            
        Returns:
            dict: Response message
        """
        try:
            response = self.session.post(f"{self.base_url}/broadcast/{equipment_id}")
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Failed to broadcast equipment ID: {e}")
            return {"error": str(e)}
    
    def get_game_state(self) -> Dict:
        """
        Get current game state including all player scores and team totals.
        
        Returns:
            dict: Game state data with structure:
            {
                "is_active": true,
                "red_team": {
                    "players": [{"equipment_id": 1, "codename": "Player1", "score": 10, "hit_base": false}],
                    "total_score": 10
                },
                "green_team": {...}
            }
        """
        try:
            response = self.session.get(f"{self.base_url}/game/state")
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Failed to get game state: {e}")
            return {"error": str(e)}
    
    def reset_game(self) -> Dict:
        """
        Reset game state (scores, base hits) without clearing players.
        
        Returns:
            dict: Response message
        """
        try:
            response = self.session.post(f"{self.base_url}/game/reset")
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Failed to reset game: {e}")
            return {"error": str(e)}
    
    # System Status Endpoint
    
    def check_health(self) -> Dict:
        """
        Check system health status.
        
        Returns:
            dict: Health status data
        """
        try:
            response = self.session.get(f"{self.base_url}/health")
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Failed to check health: {e}")
            return {"error": str(e), "status": "unhealthy"}


# Helper functions for team management

def team_id_generator(team_name: str, start_index: int = 0) -> int:
    """
    Generate player IDs based on team name.
    Red team gets even IDs, Green team gets odd IDs.
    
    Args:
        team_name (str): Name of the team ("Red" or "Green")
        start_index (int): Starting index for ID generation
        
    Returns:
        int: Generated player ID
    """
    base = 2 if team_name.lower() == "red" else 1
    return base + (start_index * 2)

def equipment_id_generator(team_name: str, index: int = 0) -> int:
    """
    Generate equipment IDs based on team name.
    Red team gets even IDs starting at 100, Green team gets odd IDs starting at 101.
    
    Args:
        team_name (str): Name of the team ("Red" or "Green")
        index (int): Index for ID generation
        
    Returns:
        int: Generated equipment ID
    """
    base = 100 if team_name.lower() == "red" else 101
    return base + (index * 2)

def transform_players_for_ui(players_data: Dict) -> Dict:
    """
    Transform players data from backend format to UI format with red/green teams.
    Includes both player names and IDs.
    
    Args:
        players_data: Backend players data
        
    Returns:
        Dict: UI-formatted player data with red and green teams
    """
    red_team_data = {"players": [], "player_ids": []}
    green_team_data = {"players": [], "player_ids": []}
    
    if "players" in players_data:
        for player in players_data["players"]:
            player_id = player.get("id", 0)
            codename = player.get("codename", "")
            
            # Even IDs for Red team, Odd IDs for Green team
            if player_id % 2 == 0:
                red_team_data["players"].append(codename)
                red_team_data["player_ids"].append(player_id)
            else:
                green_team_data["players"].append(codename)
                green_team_data["player_ids"].append(player_id)
    
    return {
        "red_team": red_team_data,
        "green_team": green_team_data
    }
