import logging
from threading import Lock
from datetime import datetime
from collections import deque

logger = logging.getLogger(__name__)

class GameState:
    """
    Manages the game state including player scores, teams, and equipment mappings.
    Implemented as a singleton to ensure one source of truth.
    """
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Prevent re-initialization
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        
        self.lock = Lock()
        self.players = {}  # equipment_id -> {player_id, codename, team, score, hit_base}
        self.is_game_active = False
        self.events = deque(maxlen=50)  # Keep last 50 events for action log
        
    def add_player(self, equipment_id, player_id, codename, team):
        """
        Add a player to the game state
        
        Args:
            equipment_id: Equipment ID assigned to the player
            player_id: Database player ID
            codename: Player's codename
            team: 'red' or 'green'
        """
        with self.lock:
            self.players[equipment_id] = {
                'player_id': player_id,
                'codename': codename,
                'team': team,
                'score': 0,
                'hit_base': False
            }
            logger.info(f"Added player {codename} (ID: {player_id}, Equipment: {equipment_id}) to {team} team")
    
    def get_player(self, equipment_id):
        """Get player info by equipment ID"""
        with self.lock:
            return self.players.get(equipment_id)
    
    def get_all_players(self):
        """Get all players"""
        with self.lock:
            return dict(self.players)
    
    def update_score(self, equipment_id, points, event_message=None):
        """
        Update a player's score
        
        Args:
            equipment_id: Equipment ID of the player
            points: Points to add (can be negative)
            event_message: Optional custom message for event log
        
        Returns:
            New score or None if player not found
        """
        with self.lock:
            if equipment_id in self.players:
                old_score = self.players[equipment_id]['score']
                self.players[equipment_id]['score'] += points
                new_score = self.players[equipment_id]['score']
                
                if event_message:
                    self._add_event(event_message)
                
                logger.info(f"Player {equipment_id} score updated by {points} to {new_score}")
                return new_score
            return None
    
    def mark_base_hit(self, equipment_id):
        """Mark that a player hit a base"""
        with self.lock:
            if equipment_id in self.players:
                self.players[equipment_id]['hit_base'] = True
                logger.info(f"Player {equipment_id} marked as hitting base")
                return True
            return False
    
    def is_friendly_fire(self, attacker_equipment_id, victim_equipment_id):
        """
        Check if this is a friendly fire incident
        
        Args:
            attacker_equipment_id: Equipment ID of the attacker
            victim_equipment_id: Equipment ID of the victim
            
        Returns:
            True if same team, False otherwise
        """
        with self.lock:
            attacker = self.players.get(attacker_equipment_id)
            victim = self.players.get(victim_equipment_id)
            
            if not attacker or not victim:
                return False
            
            return attacker['team'] == victim['team']
    
    def get_team_score(self, team):
        """
        Get total score for a team
        
        Args:
            team: 'red' or 'green'
            
        Returns:
            Total team score
        """
        with self.lock:
            total = 0
            for player in self.players.values():
                if player['team'] == team:
                    total += player['score']
            return total
    
    def start_game(self):
        """Mark game as active"""
        with self.lock:
            self.is_game_active = True
            logger.info("Game started")
    
    def end_game(self):
        """Mark game as inactive"""
        with self.lock:
            self.is_game_active = False
            logger.info("Game ended")
    
    def reset_game(self):
        """Reset all game state"""
        with self.lock:
            for player in self.players.values():
                player['score'] = 0
                player['hit_base'] = False
            self.is_game_active = False
            logger.info("Game state reset")
    
    def clear_all_players(self):
        """Clear all players from game state"""
        with self.lock:
            self.players.clear()
            self.is_game_active = False
            self.events.clear()
            logger.info("All players cleared from game state")
    
    def _add_event(self, message, event_type="info"):
        """Add event to history (internal use, assumes lock is held)"""
        event = {
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'message': message,
            'type': event_type
        }
        self.events.append(event)
    
    def add_event(self, message, event_type="info"):
        """Add event to history (thread-safe public method)"""
        with self.lock:
            self._add_event(message, event_type)
    
    def get_recent_events(self, count=10):
        """Get recent events for display"""
        with self.lock:
            # Return most recent events (last 'count' items)
            return list(self.events)[-count:]
