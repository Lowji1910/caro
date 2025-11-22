"""
Shared state for socket modules to avoid circular imports.
"""

# Global matchmaking queue
matchmaking_queue = {
    'tic-tac-toe': [],
    'caro': []
}

# Global games state
games = {}

# Global mapping for disconnect handling
SID_TO_ROOM = {}

def get_games():
    """Get current games state."""
    return games

def get_matchmaking_queue():
    """Get current matchmaking queues."""
    return matchmaking_queue
