"""
Game socket handlers: Move processing, AI moves, game end handling.
"""
from flask import request
from flask_socketio import emit
from game.engine import GameEngine
from game.ai import AIPlayer
from services.rank_service import RankService
from services.match_service import MatchService
from sockets.matchmaking import get_games


def register_game_handlers(socketio):
    """Register game socket event handlers."""
    
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection."""
        print(f'Client connected: {request.sid}')
    
    @socketio.on('make_move')
    def handle_move(data):
        """
        Handle player move.
        
        Data:
            - roomId: str
            - r: int (row)
            - c: int (column)
            - player: int (1 or 2)
        """
        room_id = data.get('roomId')
        r, c = data.get('r'), data.get('c')
        player = data.get('player')
        
        games = get_games()
        game = games.get(room_id)
        if not game:
            return
        
        # Validate move
        if game['turn'] != player:
            return
        
        if not GameEngine.is_valid_move(game['board'], r, c):
            return
        
        # Apply move
        GameEngine.apply_move(game['board'], r, c, player)
        
        # Record history
        game['history'].append({'r': r, 'c': c, 'player': player})
        
        # Check winner
        winner, winning_line = GameEngine.check_winner(
            game['board'],
            game['type'],
            {'r': r, 'c': c}
        )
        
        # Update turn
        next_player = 2 if player == 1 else 1
        game['turn'] = next_player
        
        # Broadcast game update
        emit('game_update', {
            'board': game['board'],
            'currentPlayer': next_player,
            'winner': winner,
            'winningLine': winning_line,
            'lastMove': {'r': r, 'c': c}
        }, room=room_id)
        
        # Handle end game
        if winner != 0:
            _handle_end_game(game, winner)
        # Handle AI move for practice mode
        elif game['mode'] == 'practice' and next_player == 2:
            _handle_ai_move(socketio, room_id, game)
    
    @socketio.on('send_chat')
    def handle_chat(data):
        """
        Handle chat message.
        
        Data:
            - roomId: str
            - message: str
            - sender: str
        """
        room_id = data.get('roomId')
        message = data.get('message')
        sender = data.get('sender')
        
        emit('receive_chat', {
            'sender': sender,
            'message': message
        }, room=room_id)

    @socketio.on('request_undo')
    def handle_undo_request(data):
        """
        Handle undo request from a player.
        
        Data:
            - roomId: str
        """
        room_id = data.get('roomId')
        games = get_games()
        game = games.get(room_id)
        
        if not game:
            return
            
        # Notify the other player (opponent)
        # In a 2-player room, broadcasting to the room works, but the client needs to know WHO requested.
        # But for simplicity as per spec: "Server báo cho B" -> emit 'undo_requested' to room.
        # The client logic "window.confirm" will show on both if we just emit to room?
        # No, usually we emit to the opponent. But here let's emit to room but exclude sender?
        # Flask-SocketIO 'include_self=False' or 'skip_sid=request.sid'
        emit('undo_requested', room=room_id, include_self=False)

    @socketio.on('resolve_undo')
    def handle_undo_resolve(data):
        """
        Handle opponent's decision on undo request.
        
        Data:
            - roomId: str
            - accept: boolean
        """
        room_id = data.get('roomId')
        accept = data.get('accept')
        games = get_games()
        game = games.get(room_id)
        
        if not game:
            return
            
        if not accept:
            emit('undo_declined', room=room_id, include_self=False)
            return
            
        # Perform Undo
        if not game['history']:
            return
            
        # 1. Get last move
        last_move = game['history'].pop()
        r, c = last_move['r'], last_move['c']
        prev_player = last_move['player']
        
        # 2. Undo on board
        GameEngine.undo_move(game['board'], r, c)
        
        # 3. Revert turn
        game['turn'] = prev_player
        
        # 4. Update last move for UI (need the move BEFORE the one we just undid)
        # If history is empty, lastMove is None.
        new_last_move = game['history'][-1] if game['history'] else None
        
        # 5. Broadcast update
        emit('game_update', {
            'board': game['board'],
            'currentPlayer': game['turn'],
            'winner': 0, # Assume undoing clears winner state if any
            'winningLine': None,
            'lastMove': new_last_move
        }, room=room_id)

    @socketio.on('claim_timeout')
    def handle_timeout(data):
        """
        Handle timeout claim.
        
        Data:
            - roomId: str
        """
        room_id = data.get('roomId')
        games = get_games()
        game = games.get(room_id)
        
        if not game:
            return
            
        # Determine winner (the one who claimed it, assuming they claimed because opponent ran out of time)
        # Actually, we should check whose turn it is.
        # If it is Player X's turn, and time runs out, Player O wins.
        # So if Player O claims timeout, and it IS Player X's turn, then O wins.
        
        current_turn = game['turn']
        # The winner is the OTHER player
        winner = 2 if current_turn == 1 else 1
        
        # Broadcast game end
        emit('game_update', {
            'board': game['board'],
            'currentPlayer': 0, # Game over
            'winner': winner,
            'winningLine': None,
            'lastMove': None
        }, room=room_id)
        
        _handle_end_game(game, winner)


def _handle_end_game(game, winner):
    """
    Handle game end: update ranks and save match history.
    
    Args:
        game: Game state dict
        winner: 1, 2, 'draw', or 0
    """
    if game['mode'] == 'ranked' and winner != 0:
        # Update ranks
        if winner != 'draw':
            winner_uid = game['players'][winner]
            loser_uid = game['players'][3 - winner]
            RankService.update_rank(winner_uid, 25)
            RankService.update_rank(loser_uid, -10)
        
        # Save match history
        winner_uid = None
        if winner != 'draw':
            winner_uid = game['players'][winner]
        
        p1_uid = game['players'][1]
        p2_uid = game['players'][2]
        
        MatchService.save_match(p1_uid, p2_uid, winner_uid, game['type'], game['mode'], game['history'])


def _handle_ai_move(socketio, room_id, game):
    """Handle AI move for practice mode with tuned delay per difficulty/game type."""
    difficulty = game.get('difficulty', 'medium')

    # For Tic-Tac-Toe or easy Caro, add a short artificial delay
    # For Caro medium/hard, AI computation time is already noticeable,
    # so keep additional sleep very small to avoid feeling laggy.
    if game['type'] == 'tic-tac-toe' or difficulty == 'easy':
        socketio.sleep(0.5)
    else:
        socketio.sleep(0.1)

    ai_move = AIPlayer.get_ai_move(game['board'], game['type'], difficulty)
    
    if not ai_move:
        return
    
    ar, ac = ai_move
    GameEngine.apply_move(game['board'], ar, ac, 2)
    
    ai_winner, ai_line = GameEngine.check_winner(
        game['board'],
        game['type'],
        {'r': ar, 'c': ac}
    )
    
    game['turn'] = 1
    
    emit('game_update', {
        'board': game['board'],
        'currentPlayer': 1,
        'winner': ai_winner,
        'winningLine': ai_line,
        'lastMove': {'r': ar, 'c': ac}
    }, room=room_id)
