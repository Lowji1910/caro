"""
Configuration and constants for the Ranked Arena backend.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Flask Configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'secret!')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', 5000))

# CORS Configuration
FRONTEND_ORIGIN = os.environ.get('FRONTEND_ORIGIN', '*')

# Database Configuration
DB_CONFIG = {
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'host': os.environ.get('DB_HOST', 'localhost'),
    'database': os.environ.get('DB_NAME', 'tic_tac_toe_db')
}

# Game Configuration
GAME_CONFIG = {
    'tic-tac-toe': {
        'rows': 3,
        'cols': 3,
        'win_length': 3
    },
    'caro': {
        'rows': 15,
        'cols': 20,
        'win_length': 5
    }
}

# Ranking Configuration
RANKING_CONFIG = {
    'level_up_score': 100,
    'max_level': 500,
    'win_points': 25,
    'loss_points': -10
}

# Game Directions (for winner checking)
DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]
