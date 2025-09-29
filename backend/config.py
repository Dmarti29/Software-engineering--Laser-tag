# config.py
import os

DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "/var/run/postgresql"),
    "database": os.getenv("DB_NAME", "photon"),
    "user": os.getenv("DB_USER", "student"),
    "password": os.getenv("DB_PASSWORD", "student"),    
    "port": int(os.getenv("DB_PORT", "5432")),
}

# UDP Socket Configuration 
UDP_CONFIG = {
    'broadcast_port': 7500,
    'receive_port': 7501,
    'network_address': '127.0.0.1'  # localhost
}


GAME_CONFIG = {
    'max_players_per_team': 15,
    'game_duration_minutes': 6,
    'countdown_warning_seconds': 30,
    'points_per_hit': 10,
    'points_penalty': -10,
    'base_score_points': 100
}

# Special Codes
GAME_CODES = {
    'game_start': 202,
    'game_end': 221,
    'red_base_scored': 53,
    'green_base_scored': 43
}

# File paths (for frontend team)
ASSETS_PATH = {
    'splash_logo': 'frontend/assets/logo.jpg',
    'base_icon': 'frontend/assets/base_icon.png',
    'music_directory': 'frontend/assets/music/'
}
