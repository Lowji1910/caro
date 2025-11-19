from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
import mysql.connector
from game_engine import GameEngine
import random
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Cấu hình Database
db_config = {
    'user': 'root',
    'password': '',  # Điền password của bạn
    'host': 'localhost',
    'database': 'tic_tac_toe_db'
}

# Global State
games = {} 
matchmaking_queue = {
    'tic-tac-toe': [],
    'caro': []
}
game_engine = GameEngine()

def get_db_connection():
    try:
        return mysql.connector.connect(**db_config)
    except:
        return None

def calculate_user_level(rank_score: int) -> int:
    LEVEL_UP_SCORE = 100
    MAX_LEVEL = 500
    level = (rank_score // LEVEL_UP_SCORE) + 1
    return max(1, min(MAX_LEVEL, level))

def log_level_change(cursor, user_id: int, level: int, rank_score: int):
    cursor.execute(
        """
        INSERT INTO user_levels_history (user_id, level, rank_score)
        VALUES (%s, %s, %s)
        """,
        (user_id, level, rank_score)
    )

def update_rank(user_id, points):
    conn = get_db_connection()
    if not conn: return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_level FROM users WHERE id = %s", (user_id,))
        prev_level_row = cursor.fetchone()
        prev_level = prev_level_row[0] if prev_level_row else None

        cursor.execute("UPDATE users SET rank_score = rank_score + %s WHERE id = %s", (points, user_id))
        cursor.execute("SELECT rank_score FROM users WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        if row:
            new_rank_score = row[0]
            new_level = calculate_user_level(new_rank_score)
            if prev_level != new_level:
                cursor.execute("UPDATE users SET user_level = %s WHERE id = %s", (new_level, user_id))
                log_level_change(cursor, user_id, new_level, new_rank_score)
        conn.commit()
        cursor.close()
    finally:
        conn.close()

# --- API ROUTES ---

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connect error'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    
    if not user:
        cursor.close()
        conn.close()
        return jsonify({'error': 'Invalid credentials'}), 401
    
    cursor.close()
    conn.close()
    return jsonify(user)

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    display_name = data.get('display_name')
    
    if not all([username, password, display_name]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connect error'}), 500

    cursor = conn.cursor(dictionary=True)
    
    # Check if username exists
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({'error': 'Username already exists'}), 409
    
    # Create new user
    cursor.execute("""
        INSERT INTO users (username, password, display_name, full_name) 
        VALUES (%s, %s, %s, %s)
    """, (username, password, display_name, display_name))

    user_id = cursor.lastrowid
    user = {
        'id': user_id,
        'username': username,
        'display_name': display_name,
        'full_name': display_name,
        'rank_score': 0,
        'rank_level': 'Bronze',
        'user_level': 1
    }
    log_level_change(cursor, user_id, user['user_level'], user['rank_score'])
    conn.commit()
    
    cursor.close()
    conn.close()
    return jsonify(user)

@app.route('/api/profile/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    data = request.json
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database error'}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    # Update user info
    update_fields = []
    update_values = []
    
    if 'full_name' in data:
        update_fields.append('full_name = %s')
        update_values.append(data['full_name'])
    if 'display_name' in data:
        update_fields.append('display_name = %s')
        update_values.append(data['display_name'])
    if 'date_of_birth' in data:
        update_fields.append('date_of_birth = %s')
        update_values.append(data['date_of_birth'])
    if 'bio' in data:
        update_fields.append('bio = %s')
        update_values.append(data['bio'])
    if 'user_level' in data:
        update_fields.append('user_level = %s')
        update_values.append(data['user_level'])
    
    if update_fields:
        update_values.append(user_id)
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"
        cursor.execute(query, tuple(update_values))
        conn.commit()
    
    # Return updated user
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return jsonify(user)

@app.route('/api/change-password/<int:user_id>', methods=['POST'])
def change_password(user_id):
    data = request.json
    old_password = data.get('oldPassword')
    new_password = data.get('newPassword')
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database error'}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    # Verify old password
    cursor.execute("SELECT password FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    
    if not user or user['password'] != old_password:
        cursor.close()
        conn.close()
        return jsonify({'error': 'Invalid old password'}), 401
    
    # Update password
    cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_password, user_id))
    conn.commit()
    
    cursor.close()
    conn.close()
    return jsonify({'message': 'Password changed successfully'})

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    conn = get_db_connection()
    if not conn: return jsonify([])
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, display_name, rank_score, rank_level, user_level FROM users ORDER BY rank_score DESC LIMIT 10")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@app.route('/api/history/<int:user_id>', methods=['GET'])
def get_history(user_id):
    conn = get_db_connection()
    if not conn: return jsonify([])
    
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT m.id, m.game_type, m.mode, m.winner_id, m.played_at, 
               CASE 
                 WHEN m.player1_id = %s THEN p2.display_name
                 ELSE p1.display_name
               END as opponent_name,
               CASE 
                 WHEN m.winner_id = %s THEN 'win'
                 WHEN m.winner_id IS NULL THEN 'draw'
                 ELSE 'loss'
               END as result,
               m.player1_id, m.player2_id
        FROM match_history m
        JOIN users p1 ON m.player1_id = p1.id
        JOIN users p2 ON m.player2_id = p2.id
        WHERE m.player1_id = %s OR m.player2_id = %s
        ORDER BY m.played_at DESC LIMIT 20
    """
    try:
        cursor.execute(query, (user_id, user_id, user_id, user_id))
        data = cursor.fetchall()
    except:
        data = []
        
    cursor.close()
    conn.close()
    return jsonify(data)

# --- SOCKET IO EVENTS ---

@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')

@socketio.on('join_matchmaking')
def handle_matchmaking(data):
    user_id = data.get('userId')
    game_type = data.get('type')
    mode = data.get('mode')
    difficulty = data.get('difficulty')

    # 1. Lấy tên hiển thị thật của người đang join
    conn = get_db_connection()
    current_user_name = f"Player {user_id}"
    if conn:
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT display_name FROM users WHERE id = %s", (user_id,))
            res = cur.fetchone()
            if res: current_user_name = res['display_name']
            cur.close()
            conn.close()
        except: pass

    # --- PRACTICE MODE ---
    if mode == 'practice':
        room_id = str(uuid.uuid4())
        join_room(room_id) 
        
        board = game_engine.create_board(game_type)
        games[room_id] = {
            'board': board,
            'turn': 1,
            'players': {1: user_id, 2: 'AI'},
            'type': game_type,
            'mode': 'practice',
            'difficulty': difficulty
        }
        
        emit('match_found', {
            'roomId': room_id,
            'opponent': {'display_name': f'Bot AI ({difficulty})', 'id': 'ai'},
            'firstTurn': 1,
            'board': board,
            'gameType': game_type,
            'mode': mode,
            'playerNumber': 1
        })
        return

    # --- RANKED MODE ---
    queue = matchmaking_queue[game_type]
    
    if len(queue) > 0:
        opponent = queue.pop(0)
        if opponent['userId'] == user_id:
            queue.append({'userId': user_id, 'sid': request.sid, 'display_name': current_user_name})
            return

        room_id = str(uuid.uuid4())
        
        join_room(room_id) 
        join_room(room_id, sid=opponent['sid']) 
        
        board = game_engine.create_board(game_type)
        games[room_id] = {
            'board': board,
            'turn': 1,
            'players': {1: opponent['userId'], 2: user_id}, 
            'type': game_type,
            'mode': 'ranked'
        }
        
        # FIXED: Gửi cho Player 2 (Dùng room=request.sid thay vì to=...)
        emit('match_found', {
            'roomId': room_id,
            'opponent': {'display_name': opponent['display_name'], 'id': opponent['userId']}, 
            'firstTurn': 1,
            'board': board,
            'gameType': game_type,
            'mode': mode,
            'playerNumber': 2
        }, room=request.sid)

        # FIXED: Gửi cho Player 1 (Dùng room=opponent['sid'])
        emit('match_found', {
            'roomId': room_id,
            'opponent': {'display_name': current_user_name, 'id': user_id},
            'firstTurn': 1,
            'board': board,
            'gameType': game_type,
            'mode': mode,
            'playerNumber': 1
        }, room=opponent['sid'])
        
    else:
        queue.append({'userId': user_id, 'sid': request.sid, 'display_name': current_user_name})

@socketio.on('send_chat')
def handle_chat(data):
    room_id = data.get('roomId')
    message = data.get('message')
    sender = data.get('sender')
    
    emit('receive_chat', {
        'sender': sender,
        'message': message
    }, room=room_id)

@socketio.on('make_move')
def handle_move(data):
    room_id = data.get('roomId')
    r, c = data.get('r'), data.get('c')
    player = data.get('player')
    
    game = games.get(room_id)
    if not game: return
    
    if game['turn'] != player: return
    if game['board'][r][c] != 0: return

    game['board'][r][c] = player
    
    winner, winning_line = game_engine.check_winner(game['board'], game['type'], {'r': r, 'c': c})
    
    next_player = 2 if player == 1 else 1
    game['turn'] = next_player
    
    emit('game_update', {
        'board': game['board'],
        'currentPlayer': next_player,
        'winner': winner,
        'winningLine': winning_line,
        'lastMove': {'r': r, 'c': c}
    }, room=room_id)

    # Handle End Game
    if winner != 0:
        conn = None
        try:
            # Cập nhật Rank nếu không hòa
            if game['mode'] == 'ranked' and winner != 'draw':
                winner_uid = game['players'][winner]
                loser_uid = game['players'][3-winner]
                update_rank(winner_uid, 25)
                update_rank(loser_uid, -10)

            # Lưu lịch sử (Kể cả hòa)
            if game['mode'] == 'ranked':
                winner_uid = None
                if winner != 'draw':
                    winner_uid = game['players'][winner]

                conn = get_db_connection()
                if conn:
                    cur = conn.cursor()
                    # 1=Player1, 2=Player2 -> Map sang User ID
                    p1_uid = game['players'][1]
                    p2_uid = game['players'][2]
                    
                    cur.execute("""
                        INSERT INTO match_history (player1_id, player2_id, winner_id, game_type, mode)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (p1_uid, p2_uid, winner_uid, game['type'], game['mode']))
                    conn.commit()
        except Exception as e:
            print("Error saving match:", e)
        finally:
            if conn: conn.close()
        
    # AI Move Logic
    elif game['mode'] == 'practice' and next_player == 2:
        socketio.sleep(0.5)
        difficulty = game.get('difficulty', 'medium')
        ai_move = game_engine.get_ai_move(game['board'], game['type'], difficulty)
        
        if ai_move:
            ar, ac = ai_move
            game['board'][ar][ac] = 2
            ai_winner, ai_line = game_engine.check_winner(game['board'], game['type'], {'r': ar, 'c': ac})
            game['turn'] = 1
            
            emit('game_update', {
                'board': game['board'],
                'currentPlayer': 1,
                'winner': ai_winner,
                'winningLine': ai_line,
                'lastMove': {'r': ar, 'c': ac}
            }, room=room_id)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)