import psycopg2
from psycopg2 import sql, Error
import os
from typing import Optional, List, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LaserTagDatabase:
    """
    Database handler for the Laser Tag system.
    Manages player data in PostgreSQL database.
    """
    
    def __init__(self, host="localhost", database="photon", user="postgres", password="", port=5432):
        # Initialize database connection parameters
        self.connection_params = {
            'host': host,
            'database': database,
            'user': user,
            'password': password,
            'port': port
        }
        self.connection = None
    
    def connect_to_db(self) -> bool:
        """
        Establish connection to PostgreSQL database.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.connection = psycopg2.connect(**self.connection_params)
            logger.info("Successfully connected to PostgreSQL database")
            return True
        except Error as e:
            logger.error(f"Database connection failed: {e}")
            return False
    
    def disconnect_from_db(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")
    
    def test_connection(self) -> bool:
        """
        Test database connectivity and table existence.
        """
        try:
            if not self.connection or self.connection.closed:
                if not self.connect_to_db():
                    return False
            
            cursor = self.connection.cursor()
            
            # Test if players table exists
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'players'
                );
            """)
            
            table_exists = cursor.fetchone()[0]
            cursor.close()
            
            if table_exists:
                logger.info("Database connection test successful - players table found")
                return True
            else:
                logger.error("Players table not found in database")
                return False
                
        except Error as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def get_player_by_id(self, player_id: int) -> Optional[str]:
        """
        Retrieve player codename by player ID.
        Args:
            player_id (int): Player ID to search for
        Returns:
            Optional[str]: Player codename if found, None otherwise
        """
        try:
            if not self.connection or self.connection.closed:
                if not self.connect_to_db():
                    return None
            
            cursor = self.connection.cursor()
            cursor.execute("SELECT codename FROM players WHERE id = %s", (player_id,))
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                codename = result[0]
                logger.info(f"Found player ID {player_id}: {codename}")
                return codename
            else:
                logger.info(f"Player ID {player_id} not found in database")
                return None
                
        except Error as e:
            logger.error(f"Error retrieving player {player_id}: {e}")
            return None
    
    def add_player(self, player_id: int, codename: str) -> bool:
       #adds a player to the database   
        try:
            if len(codename) > 30:
                logger.error(f"Codename too long: {codename}")
                return False
            
            if not codename.strip():
                logger.error("Codename is empty")
                return False
            
            if not self.connection or self.connection.closed:
                if not self.connect_to_db():
                    return False
            
            cursor = self.connection.cursor()
            
            # Check if player already exists
            existing_codename = self.get_player_by_id(player_id)
            
            if existing_codename:
                # Update existing player
                cursor.execute(
                    "UPDATE players SET codename = %s WHERE id = %s",
                    (codename.strip(), player_id)
                )
                logger.info(f"Updated player {player_id}: {codename}")
            else:
                cursor.execute(
                    "INSERT INTO players (id, codename) VALUES (%s, %s)",
                    (player_id, codename.strip())
                )
                logger.info(f"Added player {player_id}: {codename}")
            
            self.connection.commit()
            cursor.close()
            return True
            
        except Error as e:
            logger.error(f"Error adding player {player_id} ({codename}): {e}")
            if self.connection:
                self.connection.rollback()
            return False
    
    def clear_all_players(self) -> bool:
        """Remove all players from database (F12 functionality)."""
        try:
            if not self.connection or self.connection.closed:
                if not self.connect_to_db():
                    return False
            
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM players")
            rows_deleted = cursor.rowcount
            self.connection.commit()
            cursor.close()
            
            logger.info(f"Cleared all players from database ({rows_deleted} rows deleted)")
            return True
            
        except Error as e:
            logger.error(f"Error clearing players: {e}")
            if self.connection:
                self.connection.rollback()
            return False
    
    def get_all_players(self) -> List[Tuple[int, str]]:
        """Retrieve all players from database."""
        try:
            if not self.connection or self.connection.closed:
                if not self.connect_to_db():
                    return []
            
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, codename FROM players ORDER BY id")
            results = cursor.fetchall()
            cursor.close()
            
            logger.info(f"Retrieved {len(results)} players from database")
            return results
            
        except Error as e:
            logger.error(f"Error retrieving all players: {e}")
            return []
    
    def get_player_count(self) -> int:
       
        try:
            if not self.connection or self.connection.closed:
                if not self.connect_to_db():
                    return 0
            
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM players")
            count = cursor.fetchone()[0]
            cursor.close()
            
            return count
            
        except Error as e:
            logger.error(f"Error getting player count: {e}")
            return 0


# Convenience functions for easy integration
def create_database_connection(host="localhost", database="photon", user="postgres", password=""):
    
    db = LaserTagDatabase(host=host, database=database, user=user, password=password)
    return db
