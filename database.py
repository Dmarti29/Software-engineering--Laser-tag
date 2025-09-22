
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
            logger.error(f"Error connecting to PostgreSQL database: {e}")
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
            logger.error(f"Database connection test failed: {e}")
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
            # Validate codename length
            if len(codename) > 30:
                logger.error(f"Codename '{codename}' exceeds 30 character limit")
                return False
            
            if not codename.strip():
                logger.error("Codename cannot be empty")
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
                logger.info(f"Updated player ID {player_id}: {existing_codename} -> {codename}")
            else:
                # Insert new player
                cursor.execute(
                    "INSERT INTO players (id, codename) VALUES (%s, %s)",
                    (player_id, codename.strip())
                )
                logger.info(f"Added new player ID {player_id}: {codename}")
            
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
    """
    Create and return a LaserTagDatabase instance.
    
    Args:
        host (str): Database host
        database (str): Database name
        user (str): Database user
        password (str): Database password
        
    Returns:
        LaserTagDatabase: Database handler instance
    """
    db = LaserTagDatabase(host=host, database=database, user=user, password=password)
    return db


# Example usage and testing
if __name__ == "__main__":
    """
    Test the database functionality
    """ 
    print("Testing Laser Tag Database Module")
    print("=" * 40)
    
    # Create database instance
    db = LaserTagDatabase()
    
    # Test connection
    print("1. Testing database connection...")
    if db.test_connection():
        print("✓ Database connection successful")
    else:
        print("✗ Database connection failed")
        exit(1)
    
    print("\n2. Testing player addition...")
    
    # Add first test player
    if db.add_player(100, "TestPlayer1"):
        print("✓ Added TestPlayer1 (ID: 100)")
    else:
        print("✗ Failed to add TestPlayer1")
    
    # Add second test player
    if db.add_player(101, "TestPlayer2"):
        print("✓ Added TestPlayer2 (ID: 101)")
    else:
        print("✗ Failed to add TestPlayer2")
    
    # Test retrieving players
    print("\n3. Testing player retrieval...")
    codename = db.get_player_by_id(100)
    if codename:
        print(f"✓ Retrieved player 100: {codename}")
    else:
        print("✗ Failed to retrieve player 100")
    
    # Test getting all players
    print("\n4. Testing get all players...")
    all_players = db.get_all_players()
    print(f"Total players in database: {len(all_players)}")
    for player_id, codename in all_players:
        print(f"  ID: {player_id}, Codename: {codename}")
    
    # Test clearing players (uncomment to test)
 
    db.disconnect_from_db()
    print("\n✓ Database testing completed")
