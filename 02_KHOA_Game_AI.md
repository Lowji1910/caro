# 📗 PHẦN HỌC CỦA LÊ ĐĂNG KHOA
## Game Logic & AI System

---

## 🎯 Vai Trò Của Bạn

Bạn chịu trách nhiệm **bộ não của game** - phần logic kiểm tra thắng thua và hệ thống AI thông minh. Đây là phần quan trọng nhất quyết định ải có hợp lệ, ai thắng ai thua, và làm sao AI có thể chơi game một cách thông minh. Bạn sẽ làm việc với thuật toán nổi tiếng **Minimax** và kỹ thuật tối ưu **Alpha-Beta Pruning**.

---

## 📚 Kiến Thức Cần Nắm

### 1. Thuật Toán Minimax - Nền Tảng AI Game

Minimax là thuật toán tìm nước đi tối ưu bằng cách **giả định đối thủ cũng chơi tối ưu**.

#### **Ý Tưởng Cốt Lõi**

Tưởng tượng bạn chơi cờ caro:
1. Bạn có thể đi 10 nước khác nhau
2. Với mỗi nước đi của bạn, đối thủ lại có 9 nước đi
3. Rồi bạn lại có 8 nước đi tiếp theo...

Minimax sẽ **duyệt hết** tất cả các khả năng này và chọn nước đi tốt nhất.

#### **Cách Hoạt Động**

```
       Lượt Max (AI)
      /      |      \
    -1       5       3     ← Điểm của mỗi nước đi
   / \      / \     / \
  -1  0    2  5    3  -2   Lượt Min (Human)
```

- **Max Layer** (AI): Chọn nước đi có điểm **cao nhất**
- **Min Layer** (Human): Chọn nước đi có điểm **thấp nhất** (vì muốn AI thua)

**Ví dụ cụ thể với Tic-Tac-Toe**:

```python
def minimax(board, depth, is_maximizing):
    # Nếu game kết thúc, trả về điểm
    winner = check_winner(board)
    if winner == AI: return 100
    if winner == HUMAN: return -100
    if is_draw(board): return 0
    
    if is_maximizing:  # Lượt AI
        best_score = -infinity
        for move in get_possible_moves(board):
            board[move] = AI
            score = minimax(board, depth+1, False)
            board[move] = EMPTY  # Undo move
            best_score = max(best_score, score)
        return best_score
    
    else:  # Lượt Human
        best_score = +infinity
        for move in get_possible_moves(board):
            board[move] = HUMAN
            score = minimax(board, depth+1, True)
            board[move] = EMPTY
            best_score = min(best_score, score)
        return best_score
```

**Giải thích**:
- AI muốn **maximize** điểm → chọn `max()`
- Human muốn **minimize** điểm của AI → chọn `min()`
- Đệ quy cho đến khi game kết thúc hoặc đạt depth limit

**Độ phức tạp**: O(b^d) với b = số nước đi mỗi lượt, d = độ sâu
- Tic-Tac-Toe: 9^9 = 387,420,489 nodes (có thể duyệt hết)
- Caro: 300^20 = không tưởng → cần Alpha-Beta Pruning + heuristic

### 2. Alpha-Beta Pruning - Tối Ưu Minimax

Kỹ thuật cắt tỉa các nhánh không cần thiết.

#### **Ý Tưởng**

```
         Max
        /   \
      3      ?
     / \
    3   5
```

Giả sử đang ở Max layer, đã tìm được nước đi cho điểm 3.

Bây giờ xét nhánh phải `?`:
- Vào Min layer bên trong
- Min tìm được điểm 2
- → Min sẽ chọn <=2 (vì Min muốn điểm thấp)
- → Max không bao giờ chọn nhánh `?` này (vì đã có nhánh 3 tốt hơn)
- → **Cắt bỏ** nhánh `?`, không cần duyệt nữa

#### **Cách Implement**

```python
def minimax(board, depth, alpha, beta, is_maximizing):
    if game_over: return evaluate(board)
    
    if is_maximizing:
        max_score = -infinity
        for move in moves:
            score = minimax(board, depth+1, alpha, beta, False)
            max_score = max(max_score, score)
            alpha = max(alpha, score)
            if beta <= alpha:  # Pruning!
                break
        return max_score
    else:
        min_score = +infinity
        for move in moves:
            score = minimax(board, depth+1, alpha, beta, True)
            min_score = min(min_score, score)
            beta = min(beta, score)
            if beta <= alpha:  # Pruning!
                break
        return min_score
```

**Hiệu quả**: Giảm từ O(b^d) xuống O(b^(d/2)) trong trường hợp tốt nhất!

### 3. Heuristic Evaluation - Đánh Giá Vị Trí

Vì không thể duyệt hết cây game với Caro, cần hàm đánh giá vị trí:

```python
def evaluate_board(board):
    score = 0
    
    # Quét tất cả các hàng/cột/chéo
    for line in all_lines(board):
        ai_count = count_ai_pieces(line)
        human_count = count_human_pieces(line)
        
        # Nếu line có cả AI và Human → không tính (bị block)
        if ai_count > 0 and human_count > 0:
            continue
        
        # Tính điểm cho AI
        if ai_count == 4: score += 100000  # Sắp thắng
        elif ai_count == 3: score += 1000
        elif ai_count == 2: score += 10
        
        # Trừ điểm nếu Human có line
        if human_count == 4: score -= 100000
        elif human_count == 3: score -= 1000
        elif human_count == 2: score -= 10
    
    return score
```

**Trong project Caro**, có các patterns đặc biệt:
- **Open 4** (4 ô liên tiếp, 2 đầu trống): 100,000 điểm
- **Blocked 4**: 1,000 điểm
- **Open 3**: 500 điểm
- ...

### 4. Game State Representation

Bàn cờ được biểu diễn bằng mảng 2D:

```python
# Tic-Tac-Toe (3x3)
board = [
    [0, 1, 0],
    [2, 1, 0],
    [0, 0, 2]
]

# Caro (15x20)
board = [[0] * 20 for _ in range(15)]
```

**Quy ước**:
- `0`: Ô trống
- `1`: Player 1 (X)
- `2`: Player 2 (O)

---

## 📂 Files Bạn Phụ Trách

### 1. `backend/game/engine.py` (149 dòng) - Game Engine

**Vai trò**: Core logic của game - tạo bàn cờ, kiểm tra valid move, check winner

**Các hàm chính**:

#### `create_board(game_type)`
Tạo bàn cờ trống theo loại game:
```python
def create_board(game_type):
    config = GAME_CONFIG.get(game_type)
    rows = config['rows']  # 3 (ttt) hoặc 15 (caro)
    cols = config['cols']  # 3 (ttt) hoặc 20 (caro)
    return [[0 for _ in range(cols)] for _ in range(rows)]
```

#### `is_valid_move(board, r, c)`
Kiểm tra nước đi có hợp lệ không:
```python
def is_valid_move(board, r, c):
    rows = len(board)
    cols = len(board[0])
    
    # Ngoài biên?
    if not (0 <= r < rows and 0 <= c < cols):
        return False
    
    # Ô đã có quân?
    return board[r][c] == 0
```

#### `apply_move(board, r, c, player)`
Đặt quân lên bàn cờ:
```python
def apply_move(board, r, c, player):
    if not is_valid_move(board, r, c):
        return False
    board[r][c] = player
    return True
```

#### `check_winner(board, game_type, last_move)` - QUAN TRỌNG NHẤT!

Kiểm tra thắng/thua sau nước đi cuối:

```python
def check_winner(board, game_type, last_move):
    if not last_move:
        return 0, None
    
    r, c = last_move['r'], last_move['c']
    player = board[r][c]
    win_len = GAME_CONFIG[game_type]['win_length']  # 3 hoặc 5
    
    # Kiểm tra 4 hướng: ngang, dọc, chéo xuống, chéo lên
    for dr, dc in [(0,1), (1,0), (1,1), (1,-1)]:
        line = [(r, c)]
        
        # Đếm tiến
        for i in range(1, win_len):
            nr, nc = r + dr*i, c + dc*i
            if in_bounds(nr, nc) and board[nr][nc] == player:
                line.append((nr, nc))
            else:
                break
        
        # Đếm lùi
        for i in range(1, win_len):
            nr, nc = r - dr*i, c - dc*i
            if in_bounds(nr, nc) and board[nr][nc] == player:
                line.append((nr, nc))
            else:
                break
        
        # Nếu đủ win_length → thắng!
        if len(line) >= win_len:
            return player, line
    
    # Kiểm tra hòa (board đầy)
    if all(board[row][col] != 0 for row in range(rows) for col in range(cols)):
        return 'draw', None
    
    return 0, None  # Chưa kết thúc
```

**Vị trí**: `c:\xampp\htdocs\Caro\backend\game\engine.py`

### 2. `backend/game/ai.py` (683 dòng) - AI Logic

**Vai trò**: Thuật toán AI cho cả Tic-Tac-Toe và Caro

**Entry Point**:

```python
def get_ai_move(board, game_type, difficulty):
    if game_type == 'tic-tac-toe':
        return _get_tictactoe_move(board, difficulty)
    else:  # caro
        return _get_caro_move(board, difficulty)
```

**Cho Tic-Tac-Toe**:

#### `_get_tictactoe_move(board, difficulty)`
```python
def _get_tictactoe_move(board, difficulty):
    if difficulty == 'easy':
        # Ngẫu nhiên 100%
        moves = get_empty_cells(board)
        return random.choice(moves)
    
    elif difficulty == 'medium':
        # 30% ngẫu nhiên, 70% Minimax
        if random.random() < 0.3:
            return random.choice(get_empty_cells(board))
        # Fall through to Minimax
    
    # Hard hoặc Medium (70% case)
    return _full_minimax_ttt(board)
```

#### `_minimax_ttt(board, depth, is_maximizing, alpha, beta)`
```python
def _minimax_ttt(board, depth, is_maximizing, alpha, beta, cache):
    # Check cache để tránh tính lại
    state = serialize(board)
    if state in cache:
        return cache[state]
    
    # Check kết thúc
    winner = _check_winner_simple(board)
    if winner == 2: return 10 - depth  # AI thắng
    if winner == 1: return depth - 10  # Human thắng
    if winner == 'draw': return 0
    
    if is_maximizing:  # AI
        max_score = -infinity
        for r, c in get_empty_cells(board):
            board[r][c] = 2
            score = _minimax_ttt(board, depth+1, False, alpha, beta, cache)
            board[r][c] = 0
            max_score = max(max_score, score)
            alpha = max(alpha, score)
            if beta <= alpha: break  # Pruning
        cache[state] = max_score
        return max_score
    else:  # Human
        min_score = infinity
        for r, c in get_empty_cells(board):
            board[r][c] = 1
            score = _minimax_ttt(board, depth+1, True, alpha, beta, cache)
            board[r][c] = 0
            min_score = min(min_score, score)
            beta = min(beta, score)
            if beta <= alpha: break
        cache[state] = min_score
        return min_score
```

**Cho Caro**:

#### `_get_caro_move(board, difficulty)`
```python
def _get_caro_move(board, difficulty):
    moves = _get_neighbor_moves(board, radius=2)  # Chỉ xét ô gần quân cờ
    
    if difficulty == 'easy':
        return random.choice(moves)
    
    # Medium: depth 1, Hard: depth 2
    depth = 1 if difficulty == 'medium' else 2
    
    # Tìm nước thắng ngay
    win_move = _find_immediate_caro_move(board, moves, player=2)
    if win_move: return win_move
    
    # Chặn đối thủ thắng ngay
    block_move = _find_immediate_caro_move(board, moves, player=1)
    if block_move: return block_move
    
    # Tìm nước tạo open-4 (thắng chắc)
    vcf_move = _find_vcf_move(board, moves, player=2)
    if vcf_move: return vcf_move
    
    # Minimax với depth limit
    best_move = None
    best_score = -infinity
    
    # Sort moves theo urgency
    moves = _order_moves_by_urgency(board, moves, player=2, limit=15)
    
    for r, c in moves:
        board[r][c] = 2
        score = _minimax_caro(board, depth, False, -infinity, infinity, (r,c))
        board[r][c] = 0
        if score > best_score:
            best_score = score
            best_move = (r, c)
    
    return best_move
```

**Vị trí**: `c:\xampp\htdocs\Caro\backend\game\ai.py`

### 3. `components/GameBoard.tsx` (216 dòng) - UI Bàn Cờ

**Vai trò**: Hiển thị bàn cờ và xử lý click của user

**Các features**:
- Render 3x3 grid cho Tic-Tac-Toe
- Render 15x20 grid cho Caro
- Drag-to-pan cho Caro (kéo bàn cờ)
- Highlight winning line
- Hiển thị last move
- Undo button

**Vị trí**: `c:\xampp\htdocs\Caro\components\GameBoard.tsx`

---

## 🔄 Luồng Hoạt Động Chi Tiết

### A. Luồng Kiểm Tra Thắng/Thua

**Bước 1: Player đặt quân**
- Frontend gửi socket event `make_move` với `(r, c, player)`
- Backend nhận trong `sockets/game.py`

**Bước 2: Validate và apply move**
```python
# In sockets/game.py
game = games[room_id]
board = game['board']

# Kiểm tra valid
if not GameEngine.is_valid_move(board, r, c):
    return  # Ignore invalid move

# Apply move
GameEngine.apply_move(board, r, c, player)
game['history'].append({'r': r, 'c': c, 'player': player})
```

**Bước 3: Check winner**
```python
winner, winning_line = GameEngine.check_winner(
    board, 
    game_type='caro', 
    last_move={'r': r, 'c': c}
)
```

**Bước 4: Xử lý kết quả**
```python
if winner != 0:  # Có người thắng hoặc hòa
    _handle_end_game(game, winner)
    # → Update rank points, save match history
else:
    # Chuyển lượt
    game['turn'] = 3 - game['turn']  # 1→2, 2→1
```

**Bước 5: Emit về clients**
```python
socketio.emit('game_update', {
    'board': board,
    'currentPlayer': game['turn'],
    'winner': winner,
    'winningLine': winning_line,
    'lastMove': {'r': r, 'c': c}
}, room=room_id)
```

### B. Luồng AI Move (Practice Mode)

**Bước 1: Phát hiện lượt AI**
```python
# In sockets/game.py sau khi human move
if game['mode'] == 'practice' and game['turn'] == 2:
    _handle_ai_move(socketio, room_id, game)
```

**Bước 2: Tính nước đi AI**
```python
def _handle_ai_move(socketio, room_id, game):
    board = game['board']
    difficulty = game['difficulty']
    game_type = game['type']
    
    # Delay tùy độ khó
    delay = {
        'easy': 0.3,
        'medium': 0.6,
        'hard': 1.0
    }[difficulty]
    
    time.sleep(delay)  # Giả lập AI "suy nghĩ"
    
    # Gọi AI
    r, c = AIPlayer.get_ai_move(board, game_type, difficulty)
```

**Bước 3: Apply AI move**
```python
    GameEngine.apply_move(board, r, c, 2)
    game['history'].append({'r': r, 'c': c, 'player': 2})
    
    # Check winner
    winner, winning_line = GameEngine.check_winner(
        board, game_type, {'r': r, 'c': c}
    )
    
    # Emit update
    socketio.emit('game_update', {
        'board': board,
        'currentPlayer': 1,  # Chuyển lại lượt human
        'winner': winner,
        'winningLine': winning_line,
        'lastMove': {'r': r, 'c': c}
    }, room=room_id)
```

### C. Luồng Minimax Chi Tiết (Tic-Tac-Toe)

**Ví dụ cụ thể**:

```
Board hiện tại:
X | O | 
---------
  | X | 
---------
  |   | O

AI = X, Human = O, Lượt AI
```

**Bước 1: Liệt kê nước đi**
Empty cells: (0,2), (1,0), (2,0), (2,1)

**Bước 2: Duyệt từng nước**
```python
for r, c in empty_cells:
    board[r][c] = 2  # Thử đặt X
    score = minimax(board, depth+1, False, -inf, +inf)
    board[r][c] = 0  # Undo
    
    if score > best_score:
        best_score = score
        best_move = (r, c)
```

**Bước 3: Đệ quy sâu hơn**
Giả sử thử (0,2):
```
X | O | X  ← Thử nước này
---------
  | X | 
---------
  |   | O

→ Giờ lượt Human (Min layer)
→ Human thử (1,0):
  X | O | X
  ---------
  O | X | 
  ---------
    |   | O
  
  → Giờ lại lượt AI (Max layer)
  → AI thử (2,0):
    X | O | X
    ---------
    O | X | 
    ---------
    X |   | O
    
    → Check winner: X thắng (cột đầu tiên)
    → Return +10
```

**Bước 4: Backpropagation**
- Từ lá (X thắng, +10) bubble up về root
- Min layer sẽ chọn min của các nhánh con
- Max layer sẽ chọn max của các nhánh con

**Bước 5: Chọn nước đi tốt nhất**
```python
# Sau khi duyệt hết, best_move là nước có điểm cao nhất
return best_move
```

---

## 📋 Bảng Các Hàm Quan Trọng

| Hàm | File | Tham số | Chức năng |
|-----|------|---------|-----------|
| `create_board` | engine.py | game_type | Tạo bàn cờ trống (3x3 hoặc 15x20) |
| `is_valid_move` | engine.py | board, r, c | Kiểm tra nước đi có hợp lệ không |
| `apply_move` | engine.py | board, r, c, player | Đặt quân lên bàn cờ |
| `check_winner` | engine.py | board, game_type, last_move | Kiểm tra thắng/thua/hòa |
| `undo_move` | engine.py | board, r, c | Xóa quân (dùng cho undo request) |
| `get_ai_move` | ai.py | board, game_type, difficulty | Entry point - lấy nước đi AI |
| `_get_tictactoe_move` | ai.py | board, difficulty | AI cho Tic-Tac-Toe |
| `_get_caro_move` | ai.py | board, difficulty | AI cho Caro |
| `_minimax_ttt` | ai.py | board, depth, is_max, alpha, beta | Minimax cho Tic-Tac-Toe |
| `_minimax_caro` | ai.py | board, depth, is_max, alpha, beta, last_move | Minimax cho Caro |
| `_evaluate_board` | ai.py | board | Đánh giá điểm board (heuristic) |
| `_get_neighbor_moves` | ai.py | board, radius | Lấy các ô gần quân cờ (tối ưu search space) |
| `_find_immediate_caro_move` | ai.py | board, moves, player | Tìm nước thắng ngay lập tức |
| `_find_vcf_move` | ai.py | board, moves, player | Tìm nước tạo Open-4 (Victory Continuous Flow) |

---

## 🎤 Nội Dung Thuyết Trình

### 1. Giới Thiệu Vai Trò (1 phút)
"Em phụ trách phần **Game Logic và AI System**, là bộ não của game. Em đảm nhiệm 2 modules chính:
- **Game Engine** (engine.py): Kiểm tra nước đi hợp lệ, phát hiện thắng/thua
- **AI System** (ai.py): Thuật toán Minimax để AI chơi game thông minh"

### 2. Giải Thích Thuật Toán Minimax (3 phút)

**Demo với diagram**:
```
        Lượt AI (Max)
       /      |      \
      5       3       -1    ← AI chọn 5
     / \     / \     / \
    5  2    3 -5   -1 0    Lượt Human (Min)
```

**Nói**:
"Minimax hoạt động như sau: AI giả định đối thủ cũng chơi tối ưu. Ở lớp Max, AI chọn điểm cao nhất. Ở lớp Min, giả định đối thủ sẽ chọn điểm thấp nhất để AI thua.

Ví dụ với Tic-Tac-Toe:
- AI duyệt tất cả nước đi có thể
- Với mỗi nước, giả định đối thủ sẽ chơi tối ưu nhất
- Chọn nước đi dẫn đến kết quả tốt nhất cho AI

Nhưng vấn đề là độ phức tạp O(b^d) quá lớn với Caro. Nên em dùng kỹ thuật **Alpha-Beta Pruning**."

### 3. Alpha-Beta Pruning (2 phút)

**Vẽ diagram**:
```
         Max (alpha=-inf, beta=+inf)
        /         \
   Min (a=3)       Min (pruned!)
    / \             / \
   3   5           2   ?
```

**Nói**:
"Alpha-Beta Pruning cắt bỏ các nhánh không cần duyệt:
- `alpha`: Điểm tốt nhất mà Max đã tìm được
- `beta`: Điểm tốt nhất mà Min đã tìm được
- Nếu `beta <= alpha`: không cần duyệt nữa, cắt bỏ nhánh

Trong thực tế, kỹ thuật này giảm từ O(b^d) xuống O(b^(d/2), giúp AI Caro chạy được với depth=2."

### 4. Luồng Check Winner (1.5 phút)

**Demo code + giải thích**:
```python
def check_winner(board, game_type, last_move):
    r, c = last_move['r'], last_move['c']
    player = board[r][c]
    win_len = 5  # Cho Caro
    
    # Kiểm tra 4 hướng
    for dr, dc in [(0,1), (1,0), (1,1), (1,-1)]:
        line = [(r, c)]
        
        # Đếm tiến + đếm lùi
        # Nếu len(line) >= 5 → thắng!
```

**Nói**:
"Hàm `check_winner` kiểm tra sau mỗi nước đi:
1. Lấy vị trí nước đi cuối
2. Duyệt 4 hướng: ngang, dọc, 2 đường chéo
3. Với mỗi hướng: đếm tiến và đếm lùi
4. Nếu đủ 5 (hoặc 3 với Tic-Tac-Toe) → có người thắng
5. Nếu board đầy mà không ai thắng → hòa"

### 5. Độ Khó AI (1 phút)

"Em implement 3 mức độ khó:
- **Easy**: Random moves hoặc depth=1
- **Medium**: Minimax depth=3 (Tic-Tac-Toe) hoặc depth=1 (Caro)
- **Hard**: Full Minimax depth=5 (Tic-Tac-Toe) hoặc depth=2 (Caro)

Với Caro em còn thêm các check đặc biệt:
- Tìm nước thắng ngay lập tức
- Chặn đối thủ thắng ngay
- Tìm nước tạo Open-4 (thắng chắc)"

### 6. Tổng Kết (0.5 phút)

"Phần Game Logic đảm bảo game chạy đúng quy tắc, phát hiện thắng thua chính xác. Phần AI tạo đối thủ thông minh cho người chơi luyện tập. Đây là nền tảng để game hoạt động."

---

## 💡 Tips Học Hiệu Quả

1. **Hiểu Minimax trước khi đọc code**
   - Xem video về Minimax trên YouTube
   - Code tự tay 1 Minimax đơn giản cho Tic-Tac-Toe

2. **Trace code bằng debugger**
   - Đặt breakpoint trong `_minimax_ttt`
   - Xem board thay đổi như thế nào qua mỗi recursive call

3. **Test với các case đơn giản**
   - Board AI sắp thắng → xem AI có chọn đúng không
   - Board Human sắp thắng → xem AI có chặn không

4. **Vẽ diagram**
   - Vẽ cây Minimax cho 1 board đơn giản
   - Tính tay điểm của mỗi nhánh để hiểu logic

---

Chúc bạn học tốt! Minimax là thuật toán cổ điển nhưng cực kỳ hay! 🎮
