"""
Game socket handlers: Move processing, AI moves, game end handling.
"""
from flask import request
from flask_socketio import emit
from game.engine import GameEngine
from game.ai import AIPlayer
from services.rank_service import RankService
from services.match_service import MatchService
from sockets.state import get_games, SID_TO_ROOM


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
        """
        room_id = data.get('roomId')
        message = data.get('message', '').strip()
        sender = data.get('sender')
        sender_id = data.get('senderId')
        
        # Validation
        if not message or len(message) > 200:
            return
        
        # Sanitize (escape HTML special characters)
        import html
        message = html.escape(message)
        
        emit('receive_chat', {
            'sender': sender,
            'senderId': sender_id,
            'message': message
        }, room=room_id)

    @socketio.on('request_undo')
    def handle_undo_request(data):
        """
        Handle undo request from a player.
        """
        room_id = data.get('roomId')
        games = get_games()
        game = games.get(room_id)
        
        if not game:
            return
            
        # Notify the other player (opponent)
        emit('undo_requested', room=room_id, include_self=False)

    @socketio.on('resolve_undo')
    def handle_undo_resolve(data):
        """
        Handle opponent's decision on undo request.
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
        """
        room_id = data.get('roomId')
        games = get_games()
        game = games.get(room_id)
        
        if not game:
            return
            
        # Determine winner
        current_turn = game['turn']
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

    @socketio.on('leave_game')
    def handle_leave_game(data):
        """
        Handle player leaving the game explicitly.
        """
        room_id = data.get('roomId')
        print(f'[LEAVE_GAME] Player {request.sid} leaving room {room_id}')
        _handle_player_leave(room_id, request.sid)

    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection."""
        print(f'Client disconnected: {request.sid}')
        
        if request.sid in SID_TO_ROOM:
            room_id = SID_TO_ROOM[request.sid]
            print(f'[DISCONNECT] Player {request.sid} was in room {room_id}')
            _handle_player_leave(room_id, request.sid)
            del SID_TO_ROOM[request.sid]

def _handle_player_leave(room_id, sid):
    """Helper to handle player leaving logic."""
    games = get_games()
    game = games.get(room_id)
    
    print(f'[_handle_player_leave] room_id={room_id}, sid={sid}')
    
    if not game:
        print(f'[_handle_player_leave] Game not found for room {room_id}')
        return
    
    if 'winner' not in game:
        game['winner'] = 0
        
    if game.get('winner', 0) != 0:
        print(f'[_handle_player_leave] Game already over, winner={game.get("winner")}')
        return

    leaver_player = None
    if 'sids' in game:
        for p_num, p_sid in game['sids'].items():
            if p_sid == sid:
                leaver_player = p_num
                break
    
    if leaver_player is None:
        print(f'[_handle_player_leave] Could not identify leaver')
        return

    winner = 2 if leaver_player == 1 else 1
    game['winner'] = winner
    
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
    """
    if game['mode'] == 'ranked' and winner != 0:
        match_result = 'draw' # Mặc định

        # Update ranks and XP
        if winner == 'draw':
            p1_uid = game['players'][1]
            p2_uid = game['players'][2]
            RankService.update_rank(p1_uid, 0, 25)
            RankService.update_rank(p2_uid, 0, 25)
            match_result = 'draw'
        else:
            winner_uid = game['players'][winner]
            loser_uid = game['players'][3 - winner]
            RankService.update_rank(winner_uid, 25, 50)
            RankService.update_rank(loser_uid, -10, 15)
            match_result = 'win'
        
        # Save match history
        winner_uid = None
        if winner != 'draw':
            winner_uid = game['players'][winner]
        
        p1_uid = game['players'][1]
        p2_uid = game['players'][2]
        
        # Gọi hàm save_match với tham số match_result mới tính được
        MatchService.save_match(
            p1_uid, 
            p2_uid, 
            winner_uid, 
            game['type'], 
            game['mode'], 
            match_result,  # <-- Đã thêm biến này
            game['history']
        )


def _handle_ai_move(socketio, room_id, game):
    """Handle AI move for practice mode with tuned delay per difficulty/game type."""
    difficulty = game.get('difficulty', 'medium')

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
