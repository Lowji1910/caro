"""
Matchmaking socket handlers: Queue management and match finding.
"""
from flask import request
from flask_socketio import emit, join_room
from game.engine import GameEngine
from services.user_service import UserService

# Global matchmaking queue
matchmaking_queue = {
    'tic-tac-toe': [],
    'caro': []
}

# Global games state
games = {}


def register_matchmaking_handlers(socketio):
    """Register matchmaking socket event handlers."""
    
    @socketio.on('join_matchmaking')
    def handle_matchmaking(data):
        """
        Handle player joining matchmaking queue.
        
        Data:
            - userId: int
            - type: 'tic-tac-toe' or 'caro'
            - mode: 'ranked' or 'practice'
            - difficulty: 'easy', 'medium', 'hard' (for practice)
        """
        user_id = data.get('userId')
        game_type = data.get('type')
        mode = data.get('mode')
        difficulty = data.get('difficulty')
        
        # Get player's display name
        user = UserService.get_user_by_id(user_id)
        current_user_name = user['display_name'] if user else f"Player {user_id}"
        
        # --- PRACTICE MODE ---
        if mode == 'practice':
            _handle_practice_mode(socketio, user_id, game_type, difficulty, current_user_name)
            return
        
        # --- RANKED MODE ---
        _handle_ranked_mode(socketio, user_id, game_type, current_user_name)


def _handle_practice_mode(socketio, user_id, game_type, difficulty, user_name):
    """Handle practice mode match creation."""
    import uuid
    
    room_id = str(uuid.uuid4())
    join_room(room_id)
    
    board = GameEngine.create_board(game_type)
    games[room_id] = {
        'board': board,
        'turn': 1,
        'players': {1: user_id, 2: 'AI'},
        'type': game_type,
        'mode': 'practice',
        'difficulty': difficulty,
        'history': []
    }
    
    emit('match_found', {
        'roomId': room_id,
        'opponent': {'display_name': f'Bot AI ({difficulty})', 'id': 'ai'},
        'firstTurn': 1,
        'board': board,
        'gameType': game_type,
        'mode': 'practice',
        'playerNumber': 1,
        'difficulty': difficulty
    })


def _handle_ranked_mode(socketio, user_id, game_type, user_name):
    """Handle ranked mode matchmaking."""
    import uuid
    queue = matchmaking_queue[game_type]
    
    if len(queue) > 0:
        opponent = queue.pop(0)
        
        # Don't match player with themselves
        if opponent['userId'] == user_id:
            queue.append({'userId': user_id, 'sid': request.sid, 'display_name': user_name})
            return
        
        # Create match
        room_id = str(uuid.uuid4())
        join_room(room_id)
        join_room(room_id, sid=opponent['sid'])
        
        board = GameEngine.create_board(game_type)
        games[room_id] = {
            'board': board,
            'turn': 1,
            'players': {1: opponent['userId'], 2: user_id},
            'type': game_type,
            'mode': 'ranked',
            'history': []
        }
        
        # Notify Player 2 (current player)
        emit('match_found', {
            'roomId': room_id,
            'opponent': {'display_name': opponent['display_name'], 'id': opponent['userId']},
            'firstTurn': 1,
            'board': board,
            'gameType': game_type,
            'mode': 'ranked',
            'playerNumber': 2
        }, room=request.sid)
        
        # Notify Player 1 (opponent from queue)
        emit('match_found', {
            'roomId': room_id,
            'opponent': {'display_name': user_name, 'id': user_id},
            'firstTurn': 1,
            'board': board,
            'gameType': game_type,
            'mode': 'ranked',
            'playerNumber': 1
        }, room=opponent['sid'])
    else:
        # Add to queue
        queue.append({'userId': user_id, 'sid': request.sid, 'display_name': user_name})


def get_games():
    """Get current games state."""
    return games


def get_matchmaking_queue():
    """Get current matchmaking queues."""
    return matchmaking_queue
