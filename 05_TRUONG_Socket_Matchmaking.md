# 📘 PHẦN HỌC CỦA TÔ NGUYỄN THIÊN TRƯỜNG
## Socket & Matchmaking System

---

## 🎯 Vai Trò Của Bạn

Bạn chịu trách nhiệm **hệ thống giao tiếp realtime** - phần đảm bảo game multiplayer hoạt động mượt mà. Bạn sẽ làm việc với Socket.IO để xử lý matchmaking (ghép cặp đối thủ), game events (nước đi, chat, undo, timeout), và đồng bộ trạng thái game realtime giữa các players. Đây là phần "huyết mạch" của multiplayer game.

---

## 📚 Kiến Thức Cần Nắm

### 1. WebSocket - Giao Thức Realtime

HTTP truyền thống là **request-response**:
```
Client → Request → Server
Client ← Response ← Server
```

Vấn đề: Client không thể nhận data từ server nếu không gửi request.

**WebSocket** giải quyết bằng **bidirectional connection**:
```
Client ⇄ Server (kết nối 2 chiều, luôn mở)
```

#### **Cách Hoạt Động**

1. **Handshake**: Client gửi HTTP request upgrade lên WebSocket
2. **Connection**: Server chấp nhận, connection được giữ mở
3. **Communication**: Cả 2 bên có thể gửi message bất cứ lúc nào
4. **Close**: Khi một bên đóng connection

#### **So Sánh HTTP vs WebSocket**

| HTTP | WebSocket |
|------|-----------|
| Request-response | Bidirectional |
| Phải polling để nhận update | Server push ngay lập tức |
| Overhead cao (headers mỗi request) | Overhead thấp sau khi connect |
| Phù hợp cho REST APIs | Phù hợp cho realtime apps |

### 2. Socket.IO - Framework Trên WebSocket

Socket.IO là library JavaScript/Python làm WebSocket dễ hơn.

#### **Server Side (Python)**

```python
from flask_socketio import SocketIO, emit, join_room

socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    print(f"Client {request.sid} connected")
    # request.sid = Session ID của client

@socketio.on('my_event')
def handle_event(data):
    print(f"Received: {data}")
    emit('response', {'msg': 'Got it!'})

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client {request.sid} disconnected")
```

#### **Client Side (JavaScript/TypeScript)**

```typescript
import { io } from 'socket.io-client';

const socket = io('http://localhost:5000');

socket.on('connect', () => {
  console.log('Connected to server');
});

socket.emit('my_event', { data: 'Hello' });

socket.on('response', (data) => {
  console.log(data.msg);  // "Got it!"
});
```

### 3. Rooms - Group Communication

**Room** là group của nhiều clients. Server có thể emit message tới tất cả clients trong room.

```python
# Client join room
join_room('room123')

# Emit tới tất cả clients trong room
emit('game_update', data, room='room123')

# Emit tới tất cả NGOẠI TRỪ sender
emit('game_update', data, room='room123', include_self=False)

# Emit tới 1 client cụ thể (dùng SID)
emit('private_message', data, room=specific_sid)
```

**Use case trong project**:
- Mỗi trận đấu = 1 room
- 2 players join room đó
- Khi một player đi nước → emit `game_update` tới room → cả 2 nhận

### 4. Event-Driven Architecture

Socket.IO hoạt động theo mô hình **event-driven**:

```python
# Server lắng nghe events từ client
@socketio.on('join_matchmaking')
def handle_matchmaking(data):
    # ...

@socketio.on('make_move')
def handle_move(data):
    # ...

# Server emit events tới client
emit('match_found', {...})
emit('game_update', {...})
```

```typescript
// Client lắng nghe events từ server
socket.on('match_found', (data) => {
  console.log('Found match!', data);
});

// Client emit events tới server
socket.emit('make_move', { r: 0, c: 0 });
```

**Lưu ý**: Event names phải khớp giữa client và server!

### 5. State Management trong Realtime Apps

Với multiplayer game, cần quản lý state của:
- Tất cả các game đang chơi
- Hàng đợi matchmaking
- Mapping giữa SID và room

```python
# In sockets/state.py
games = {}  # room_id → game state
matchmaking_queue = {
    'tic-tac-toe': [],
    'caro': []
}
SID_TO_ROOM = {}  # sid → room_id
```

**Ví dụ game state**:
```python
games['room123'] = {
    'board': [[0,0,0], [0,0,0], [0,0,0]],
    'turn': 1,  # 1 hoặc 2
    'players': {1: 42, 2: 57},  # player number → user_id
    'sids': {1: 'sid_abc', 2: 'sid_def'},
    'type': 'tic-tac-toe',
    'mode': 'ranked',
    'history': [{'r':0,'c':0,'player':1}, ...]
}
```

### 6. Concurrency Issues

Vì realtime, nhiều events có thể xảy ra đồng thời:
- Player A và Player B cùng đi nước 1 lúc
- Player A leave game ngay khi Player B vừa đi

**Giải pháp**:
1. **Check turn**: Chỉ cho phép player đi khi đến lượt
2. **Validate state**: Kiểm tra game còn active không
3. **Locks** (nếu cần): Đảm bảo 1 operation hoàn thành trước khi bắt đầu operation khác

```python
# Check turn
if game['turn'] != player_number:
    return  # Không phải lượt của player này

# Check game active
if game.get('winner', 0) != 0:
    return  # Game đã kết thúc
```

---

## 📂 Files Bạn Phụ Trách

### 1. `backend/sockets/state.py` (15 dòng) - Shared State

**Vai trò**: Global state được share giữa các socket handlers

```python
"""Shared state for socket handlers."""

# Lưu tất cả games đang active
# Format: room_id → game_state dict
games = {}

# Hàng đợi matchmaking cho mỗi game type
# Format: game_type → list of {userId, sid, display_name}
matchmaking_queue = {
    'tic-tac-toe': [],
    'caro': []
}

# Mapping từ SID sang room_id
# Dùng để biết client đang ở room nào khi disconnect
SID_TO_ROOM = {}

def get_games():
    return games
```

**Vị trí**: `c:\xampp\htdocs\Caro\backend\sockets\state.py`

### 2. `backend/sockets/matchmaking.py` (131 dòng) - Matchmaking Logic

**Vai trò**: Xử lý tìm trận đấu (ghép đối thủ hoặc tạo game với AI)

#### `handle_matchmaking(data)`

Entry point khi client emit `join_matchmaking`:

```python
@socketio.on('join_matchmaking')
def handle_matchmaking(data):
    user_id = data.get('userId')
    game_type = data.get('type')  # 'tic-tac-toe' hoặc 'caro'
    mode = data.get('mode')  # 'ranked' hoặc 'practice'
    difficulty = data.get('difficulty')  # 'easy', 'medium', 'hard'
    
    # Lấy display name từ database
    user = UserService.get_user_by_id(user_id)
    user_name = user['display_name'] if user else f"Player {user_id}"
    
    if mode == 'practice':
        _handle_practice_mode(socketio, user_id, game_type, difficulty, user_name)
    else:
        _handle_ranked_mode(socketio, user_id, game_type, user_name)
```

#### `_handle_practice_mode()` - Tạo Game Với AI

```python
def _handle_practice_mode(socketio, user_id, game_type, difficulty, user_name):
    import uuid
    
    # Tạo room ID unique
    room_id = str(uuid.uuid4())
    
    # Client join room
    join_room(room_id)
    SID_TO_ROOM[request.sid] = room_id
    
    # Tạo board
    board = GameEngine.create_board(game_type)
    
    # Tạo game state
    games[room_id] = {
        'board': board,
        'turn': 1,
        'players': {1: user_id, 2: 'AI'},
        'sids': {1: request.sid, 2: 'ai'},
        'type': game_type,
        'mode': 'practice',
        'difficulty': difficulty,
        'history': []
    }
    
    # Emit tới client
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
```

#### `_handle_ranked_mode()` - Ghép Đối Thủ

```python
def _handle_ranked_mode(socketio, user_id, game_type, user_name):
    import uuid
    queue = matchmaking_queue[game_type]
    
    if len(queue) > 0:
        # Có người đang chờ → ghép ngay
        opponent = queue.pop(0)
        
        # Tránh tự đấu với mình
        if opponent['userId'] == user_id:
            queue.append({'userId': user_id, 'sid': request.sid, 'display_name': user_name})
            return
        
        # Tạo room
        room_id = str(uuid.uuid4())
        join_room(room_id)
        join_room(room_id, sid=opponent['sid'])
        
        SID_TO_ROOM[request.sid] = room_id
        SID_TO_ROOM[opponent['sid']] = room_id
        
        # Tạo board và game state
        board = GameEngine.create_board(game_type)
        games[room_id] = {
            'board': board,
            'turn': 1,
            'players': {1: opponent['userId'], 2: user_id},
            'sids': {1: opponent['sid'], 2: request.sid},
            'type': game_type,
            'mode': 'ranked',
            'history': []
        }
        
        # Emit tới Player 2 (current player)
        emit('match_found', {
            'roomId': room_id,
            'opponent': {'display_name': opponent['display_name'], 'id': opponent['userId']},
            'firstTurn': 1,
            'board': board,
            'gameType': game_type,
            'mode': 'ranked',
            'playerNumber': 2
        }, room=request.sid)
        
        # Emit tới Player 1 (opponent)
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
        # Chưa có ai → thêm vào queue
        queue.append({
            'userId': user_id,
            'sid': request.sid,
            'display_name': user_name
        })
```

**Vị trí**: `c:\xampp\htdocs\Caro\backend\sockets\matchmaking.py`

### 3. `backend/sockets/game.py` (371 dòng) - Game Event Handlers

**Vai trò**: Xử lý tất cả events trong game (move, chat, undo, timeout, leave)

#### `handle_move(data)` - Xử Lý Nước Đi

```python
@socketio.on('make_move')
def handle_move(data):
    room_id = data.get('roomId')
    r = data.get('r')
    c = data.get('c')
    player = data.get('player')
    
    game = games.get(room_id)
    if not game:
        return
    
    board = game['board']
    
    # Validate move
    if not GameEngine.is_valid_move(board, r, c):
        return
    
    if game['turn'] != player:
        return  # Không phải lượt của player này
    
    # Apply move
    GameEngine.apply_move(board, r, c, player)
    game['history'].append({'r': r, 'c': c, 'player': player})
    
    # Check winner
    winner, winning_line = GameEngine.check_winner(
        board,
        game['type'],
        {'r': r, 'c': c}
    )
    
    if winner != 0:
        # Game kết thúc
        _handle_end_game(game, winner)
    else:
        # Chuyển lượt
        game['turn'] = 3 - game['turn']  # 1→2, 2→1
        
        # Nếu practice mode và lượt AI → gọi AI
        if game['mode'] == 'practice' and game['turn'] == 2:
            _handle_ai_move(socketio, room_id, game)
    
    # Emit update tới cả room
    emit('game_update', {
        'board': board,
        'currentPlayer': game['turn'],
        'winner': winner,
        'winningLine': winning_line,
        'lastMove': {'r': r, 'c': c}
    }, room=room_id)
```

#### `handle_chat(data)` - Xử Lý Chat

```python
@socketio.on('send_chat')
def handle_chat(data):
    room_id = data.get('roomId')
    message = data.get('message', '').strip()
    sender = data.get('sender')
    sender_id = data.get('senderId')
    
    # Giới hạn độ dài
    if len(message) > 200:
        message = message[:200]
    
    # Sanitize HTML để tránh XSS
    import html
    message = html.escape(message)
    
    # Broadcast tới room
    emit('receive_chat', {
        'sender': sender,
        'senderId': sender_id,
        'message': message
    }, room=room_id)
```

#### `handle_undo_request(data)` - Xin Đi Lại

```python
@socketio.on('request_undo')
def handle_undo_request(data):
    room_id = data.get('roomId')
    game = games.get(room_id)
    
    if not game or game['mode'] != 'ranked':
        return  # Chỉ cho undo trong ranked
    
    # Lấy SID của đối thủ
    requester_sid = request.sid
    opponent_sid = None
    
    for pnum, sid in game['sids'].items():
        if sid != requester_sid:
            opponent_sid = sid
            break
    
    if opponent_sid:
        # Emit request tới đối thủ
        emit('undo_requested', room=opponent_sid)
```

#### `handle_undo_resolve(data)` - Phản Hồi Undo

```python
@socketio.on('resolve_undo')
def handle_undo_resolve(data):
    room_id = data.get('roomId')
    accept = data.get('accept')
    game = games.get(room_id)
    
    if not game:
        return
    
    if accept:
        # Rollback 1 nước đi
        if len(game['history']) > 0:
            last_move = game['history'].pop()
            GameEngine.undo_move(game['board'], last_move['r'], last_move['c'])
            game['turn'] = 3 - game['turn']  # Đổi lượt
            
            # Emit update
            emit('game_update', {
                'board': game['board'],
                'currentPlayer': game['turn'],
                'winner': 0,
                'winningLine': None,
                'lastMove': None
            }, room=room_id)
    else:
        # Từ chối → thông báo cho requester
        # (Cần track ai là requester, ở đây đơn giản hoá)
        for pnum, sid in game['sids'].items():
            if sid != request.sid:
                emit('undo_declined', room=sid)
```

#### `handle_timeout(data)` - Claim Timeout

```python
@socketio.on('claim_timeout')
def handle_timeout(data):
    room_id = data.get('roomId')
    game = games.get(room_id)
    
    if not game or game['mode'] != 'ranked':
        return
    
    # Client calling này = người chờ (đối thủ hết giờ)
    claimer_sid = request.sid
    claimer_player = None
    loser_player = None
    
    for pnum, sid in game['sids'].items():
        if sid == claimer_sid:
            claimer_player = pnum
        else:
            loser_player = pnum
    
    if claimer_player:
        # Claimer thắng
        _handle_end_game(game, claimer_player)
        
        emit('game_update', {
            'board': game['board'],
            'currentPlayer': game['turn'],
            'winner': claimer_player,
            'winningLine': None,
            'lastMove': None
        }, room=room_id)
```

#### `handle_leave_game(data)` - Rời Trận

```python
@socketio.on('leave_game')
def handle_leave_game(data):
    room_id = data.get('roomId')
    _handle_player_leave(room_id, request.sid)
```

#### `handle_disconnect()` - Disconnect

```python
@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    room_id = SID_TO_ROOM.get(sid)
    
    if room_id:
        _handle_player_leave(room_id, sid)
        del SID_TO_ROOM[sid]
```

**Vị trí**: `c:\xampp\htdocs\Caro\backend\sockets\game.py`

---

## 🔄 Luồng Hoạt Động Chi Tiết

### A. Luồng Matchmaking (Ranked)

**Bước 1: User 1 click "Trận Đấu Xếp Hạng"**
- Frontend emit `join_matchmaking` với `{userId: 1, type: 'caro', mode: 'ranked'}`

**Bước 2: Server nhận event**
- `handle_matchmaking()` được gọi
- Check queue của `'caro'`
- Queue trống → thêm User 1 vào queue

**Bước 3: User 2 cũng click "Trận Đấu Xếp Hạng"**
- Frontend emit `join_matchmaking` với `{userId: 2, type: 'caro', mode: 'ranked'}`

**Bước 4: Server ghép cặp**
```python
queue = matchmaking_queue['caro']
# queue = [{userId: 1, sid: 'abc', display_name: 'Player1'}]

opponent = queue.pop(0)  # Lấy User 1 ra
# Tạo room, join cả 2
# Emit 'match_found' tới cả 2
```

**Bước 5: Cả 2 clients nhận `match_found`**
- User 1 nhận: `{playerNumber: 1, opponent: {display_name: 'Player2'}, ...}`
- User 2 nhận: `{playerNumber: 2, opponent: {display_name: 'Player1'}, ...}`
- Cả 2 chuyển sang view GAME

### B. Luồng Game Move (Realtime)

**Bước 1: Player 1 (lượt của mình) click vào ô (0,0)**
- Frontend emit `make_move` với `{roomId: 'room123', r: 0, c: 0, player: 1}`

**Bước 2: Server nhận và validate**
```python
game = games['room123']
# Kiểm tra:
# - Ô (0,0) có trống không?
# - Có phải lượt của player 1 không?
```

**Bước 3: Apply move**
```python
board[0][0] = 1
game['history'].append({r:0, c:0, player:1})
```

**Bước 4: Check winner**
```python
winner, winning_line = GameEngine.check_winner(board, 'tic-tac-toe', {r:0,c:0})
# winner = 0 (chưa ai thắng)
```

**Bước 5: Chuyển lượt**
```python
game['turn'] = 2
```

**Bước 6: Emit `game_update` tới room**
```python
emit('game_update', {
    'board': [[1,0,0], [0,0,0], [0,0,0]],
    'currentPlayer': 2,
    'winner': 0,
    'lastMove': {r:0, c:0}
}, room='room123')
```

**Bước 7: Cả 2 clients nhận event**
- Board được cập nhật
- Player 2 thấy "LƯỢTsend CỦA BẠN"
- Player 1 thấy "LƯỢT ĐỐI THỦ"

### C. Luồng AI Move

**Sau khi human move trong practice mode**:

```python
# In handle_move()
if game['mode'] == 'practice' and game['turn'] == 2:
    _handle_ai_move(socketio, room_id, game)
```

**Trong `_handle_ai_move()`**:
```python
import time

# Delay tùy độ khó
delay_map = {'easy': 0.3, 'medium': 0.6, 'hard': 1.0}
time.sleep(delay_map[game['difficulty']])

# Gọi AI
from game.ai import AIPlayer
r, c = AIPlayer.get_ai_move(board, game_type, difficulty)

# Apply move
GameEngine.apply_move(board, r, c, 2)
game['history'].append({r, c, player: 2})

# Check winner
winner, winning_line = GameEngine.check_winner(board, game_type, {r, c})

# Emit update
socketio.emit('game_update', {
    'board': board,
    'currentPlayer': 1,  # Chuyển lại lượt human
    'winner': winner,
    'winningLine': winning_line,
    'lastMove': {r, c}
}, room=room_id)
```

### D. Luồng Handle End Game

**Khi có winner**:

```python
def _handle_end_game(game, winner):
    if game['mode'] != 'ranked':
        return  # Practice không tính điểm
    
    player1_id = game['players'][1]
    player2_id = game['players'][2]
    
    # Cập nhật stats và rank
    if winner == 1:
        # Player 1 thắng
        RankService.update_rank(player1_id, rank_points_delta=+25, xp_delta=+50)
        RankService.update_rank(player2_id, rank_points_delta=-10, xp_delta=+15)
        
        # Update wins/losses
        DatabaseQuery.execute_update("UPDATE users SET wins = wins + 1 WHERE id = %s", (player1_id,))
        DatabaseQuery.execute_update("UPDATE users SET losses = losses + 1 WHERE id = %s", (player2_id,))
        
        winner_id = player1_id
        
    elif winner == 2:
        # Player 2 thắng
        RankService.update_rank(player2_id, rank_points_delta=+25, xp_delta=+50)
        RankService.update_rank(player1_id, rank_points_delta=-10, xp_delta=+15)
        
        DatabaseQuery.execute_update("UPDATE users SET wins = wins + 1 WHERE id = %s", (player2_id,))
        DatabaseQuery.execute_update("UPDATE users SET losses = losses + 1 WHERE id = %s", (player1_id,))
        
        winner_id = player2_id
        
    else:  # draw
        RankService.update_rank(player1_id, rank_points_delta=0, xp_delta=+15)
        RankService.update_rank(player2_id, rank_points_delta=0, xp_delta=+15)
        
        DatabaseQuery.execute_update("UPDATE users SET draws = draws + 1 WHERE id IN (%s, %s)", (player1_id, player2_id))
        
        winner_id = None
    
    # Lưu match history
    MatchService.save_match(
        player1_id,
        player2_id,
        winner_id,
        game['type'],
        game['mode'],
        game['history'],
        duration=0  # TODO: track duration
    )
```

---

## 📋 Bảng Các Hàm Quan Trọng

| Hàm | File | Tham số | Chức năng |
|-----|------|---------|-----------|
| `handle_matchmaking` | matchmaking.py | data | Entry point cho matchmaking |
| `_handle_practice_mode` | matchmaking.py | socketio, user_id, game_type, difficulty, user_name | Tạo game với AI |
| `_handle_ranked_mode` | matchmaking.py | socketio, user_id, game_type, user_name | Ghép đối thủ hoặc thêm vào queue |
| `handle_move` | game.py | data | Xử lý nước đi của player |
| `handle_chat` | game.py | data | Broadcast tin nhắn chat |
| `handle_undo_request` | game.py | data | Gửi undo request tới đối thủ |
| `handle_undo_resolve` | game.py | data | Xử lý phản hồi undo (accept/decline) |
| `handle_timeout` | game.py | data | Claim thắng do đối thủ timeout |
| `handle_leave_game` | game.py | data | Xử lý khi player rời trận |
| `handle_disconnect` | game.py | - | Xử lý khi client disconnect |
| `_handle_end_game` | game.py | game, winner | Update rank, lưu match history |
| `_handle_ai_move` | game.py | socketio, room_id, game | Tính và apply nước đi AI |

---

## 🎤 Nội Dung Thuyết Trình

### 1. Giới Thiệu Vai Trò (1 phút)
"Em phụ trách phần **Socket và Matchmaking System**, là hệ thống realtime đảm bảo multiplayer game hoạt động. Bao gồm:
- Matchmaking: Ghép cặp đối thủ
- Game events: Move, chat, undo, timeout
- State synchronization: Đồng bộ trạng thái game giữa 2 players"

### 2. WebSocket vs HTTP (1.5 phút)

**Demo diagram**:
```
HTTP:
Client → Request → Server
       ← Response ←
(Phải gửi request mới nhận data)

WebSocket:
Client ⇄ Server
(Kết nối 2 chiều, luôn mở)
```

**Nói**:
"HTTP truyền thống chỉ là request-response. Client muốn biết đối thủ đã đi chưa phải polling liên tục → tốn bandwidth.

WebSocket tạo kết nối 2 chiều luôn mở. Server có thể push data ngay khi có event → perfect cho multiplayer game."

### 3. Matchmaking Logic (2 phút)

"Matchmaking có 2 modes:

**Practice Mode**: Đơn giản
- Tạo room ngay với AI
- Emit 'match_found' cho client
- Game bắt đầu

**Ranked Mode**: Phức tạp hơn
- Check queue của game type (tic-tac-toe hoặc caro)
- Nếu có người chờ → ghép ngay, tạo room, join cả 2
- Emit 'match_found' cho CẢ 2 với thông tin đối thủ và playerNumber
- Nếu chưa có ai → thêm vào queue

**Race condition**: Tránh user tự đấu với chính mình bằng cách check `opponent.userId != current_userId`"

**Demo code**:
```python
if len(queue) > 0:
    opponent = queue.pop(0)
    if opponent['userId'] == user_id:
        queue.append(...)  # Re-add và return
        return
    # Tạo match...
```

### 4. Game Event Handling (2 phút)

"Sau khi match found, em xử lý các events:

**make_move**:
1. Validate: ô trống? đúng lượt?
2. Apply move vào board
3. Check winner
4. Emit 'game_update' tới room → cả 2 players nhận

**send_chat**:
1. Sanitize HTML (tránh XSS)
2. Limit 200 ký tự
3. Broadcast tới room

**request_undo**:
1. Emit 'undo_requested' tới đối thủ
2. Đối thủ nhận, show confirm dialog
3. Emit 'resolve_undo' với accept=true/false
4. Nếu accept: rollback last move, emit 'game_update'

**claim_timeout**:
1. Validate: ranked mode? game đang chơi?
2. Set winner = claimer
3. _handle_end_game()

Tất cả events đều emit 'game_update' để sync state."

### 5. Rooms và Broadcasting (1 phút)

"Socket.IO Rooms là key concept:
- Mỗi trận đấu = 1 room
- Join room: `join_room('room123')`
- Emit tới room: `emit('game_update', data, room='room123')`
- Cả 2 players trong room nhận event

Ưu điểm: Không cần track manually ai trong trận nào."

### 6. State Management (1 phút)

"Em quản lý 3 dạng state:

**games**: room_id → game state (board, turn, players, history)
**matchmaking_queue**: game_type → list of waiting players
**SID_TO_ROOM**: sid → room_id (để handle disconnect)

Khi disconnect:
- Lấy room_id từ SID_TO_ROOM
- Gọi _handle_player_leave()
- Đối thủ được thông báo → thắng tự động nếu ranked"

### 7. Tổng Kết (0.5 phút)

"Socket system đảm bảo game multiplayer mượt mà, realtime, và đồng bộ giữa players. Đây là backbone của ứng dụng."

---

## 💡 Tips Học Hiệu Quả

1. **Test multiplayer với 2 tabs**
   - Mở 2 tabs, login 2 user khác nhau
   - Matchmaking và chơi với nhau
   - Quan sát WebSocket events trong DevTools (Network tab → WS)

2. **Đọc code theo event flow**
   - Trace từ `socket.emit` (client) → `@socketio.on` (server) → `emit` (server) → `socket.on` (client)

3. **Hiểu rooms**
   - Print ra `games` dict sau mỗi event
   - Xem room được tạo, players được add như thế nào

4. **Debug với console.log**
   - Log mọi socket event
   - Xem data flow: client gửi gì, server xử lý ra sao, emit về gì

Chúc bạn học tốt! Realtime communication rất thú vị! ⚡
