# 📕 PHẦN HỌC CỦA NGUYỄN VŨ TUẤN KIỆT
## Database & Ranking System

---

## 🎯 Vai Trò Của Bạn

Bạn chịu trách nhiệm **trái tim của dữ liệu** - toàn bộ hệ thống database, APIs RESTful, và logic ranking phức tạp với 500 levels + 10 tiers + 4 ranks. Bạn sẽ làm việc với MySQL để lưu trữ dữ liệu user, match history, và xử lý các calculation về XP, level, rank points. Đây là phần quan trọng đảm bảo dữ liệu được lưu chính xác và an toàn.

---

## 📚 Kiến Thức Cần Nắm

### 1. SQL và MySQL Cơ Bản

SQL (Structured Query Language) là ngôn ngữ để tương tác với database.

#### **Các Lệnh SQL Cơ Bản**

**SELECT - Lấy dữ liệu**
```sql
-- Lấy tất cả users
SELECT * FROM users;

-- Lấy chỉ một số cột
SELECT id, username, display_name FROM users;

-- Lấy user cụ thể
SELECT * FROM users WHERE id = 5;

-- Sắp xếp
SELECT * FROM users ORDER BY rank_score DESC LIMIT 100;

-- Join tables
SELECT u.display_name, m.winner_id, m.game_type
FROM users u
JOIN match_history m ON u.id = m.player1_id;
```

**INSERT - Thêm dữ liệu**
```sql
INSERT INTO users (username, password_hash, display_name, email)
VALUES ('player123', 'hashed_pw', 'Pro Player', 'player@email.com');
```

**UPDATE - Cập nhật dữ liệu**
```sql
UPDATE users
SET xp = xp + 50, rank_score = rank_score + 25
WHERE id = 10;
```

**DELETE - Xóa dữ liệu**
```sql
DELETE FROM match_history WHERE id = 100;
```

#### **WHERE Clauses và Operators**
```sql
-- Điều kiện
WHERE level >= 100
WHERE username LIKE 'player%'
WHERE rank_score BETWEEN 500 AND 1000

-- AND, OR
WHERE level > 50 AND rank_score > 1000
WHERE game_type = 'caro' OR game_type = 'tic-tac-toe'

-- IN
WHERE rank_id IN (3, 4)  -- Gold hoặc Crystal
```

### 2. Database Schema của Project

#### **Table: users**
```sql
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  display_name VARCHAR(100),
  full_name VARCHAR(100),
  email VARCHAR(100),
  bio TEXT,
  avatar_url TEXT,
  date_of_birth DATE,
  
  -- Ranking fields
  level INT DEFAULT 1,
  xp INT DEFAULT 0,
  rank_score INT DEFAULT 0,  -- Điểm xếp hạng (có thể giảm)
  rank_id INT DEFAULT 1,  -- 1=Bronze, 2=Silver, 3=Gold, 4=Crystal
  
  -- Stats
  wins INT DEFAULT 0,
  losses INT DEFAULT 0,
  draws INT DEFAULT 0,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Các trường quan trọng**:
- `xp`: Kinh nghiệm (chỉ tăng, không giảm) → quyết định `level`
- `level`: Cấp độ từ 1-500
- `rank_score`: Điểm rank (có thể tăng/giảm) → quyết định `rank_id`
- `rank_id`: Hạng (1-4)

#### **Table: game_levels**
```sql
CREATE TABLE game_levels (
  level INT PRIMARY KEY,
  required_score INT NOT NULL  -- XP cần để đạt level này
);

-- Ví dụ data:
-- level 1: required_score = 0
-- level 2: required_score = 100
-- level 100: required_score = 9900
-- level 500: required_score = 379900
```

Logic: Level của user = highest level mà `user.xp >= required_score`

#### **Table: tiers**
```sql
CREATE TABLE tiers (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50),  -- 'Tân Thủ', 'Nhập Môn', 'Xuất Sắc'...
  min_level INT,
  max_level INT,
  color VARCHAR(20),  -- '#9E9E9E', '#4CAF50'...
  description TEXT
);

-- 10 tiers:
-- I: Tân Thủ (1-50)
-- II: Nhập Môn (51-100)
-- ...
-- X: Chí Tôn (451-500)
```

#### **Table: ranks**
```sql
CREATE TABLE ranks (
  id INT PRIMARY KEY,
  name VARCHAR(50),  -- 'Bronze', 'Silver', 'Gold', 'Crystal'
  min_score INT,
  max_score INT,
  color VARCHAR(20)
);

-- 1: Bronze (0-499)
-- 2: Silver (500-999)
-- 3: Gold (1000-1999)
-- 4: Crystal (2000+)
```

#### **Table: match_history**
```sql
CREATE TABLE match_history (
  id INT PRIMARY KEY AUTO_INCREMENT,
  player1_id INT,
  player2_id INT,  -- NULL nếu chơi với AI
  winner_id INT,  -- ID của người thắng, NULL nếu hòa
  game_type VARCHAR(20),  -- 'tic-tac-toe' hoặc 'caro'
  mode VARCHAR(20),  -- 'ranked' hoặc 'practice'
  moves TEXT,  -- JSON string: "[{r:0,c:0,player:1}, ...]"
  duration INT,  -- Thời gian chơi (giây)
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (player1_id) REFERENCES users(id),
  FOREIGN KEY (player2_id) REFERENCES users(id)
);
```

### 3. Python MySQL Connector

Trong Python, dùng `mysql-connector-python` để kết nối database:

```python
import mysql.connector

# Kết nối
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='tic_tac_toe_db'
)

cursor = conn.cursor(dictionary=True)  # Return rows as dict

# Query
cursor.execute("SELECT * FROM users WHERE username = %s", ('player1',))
user = cursor.fetchone()
# user = {'id': 1, 'username': 'player1', 'level': 42, ...}

# Insert
cursor.execute(
    "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
    ('newuser', 'hashed_pw')
)
conn.commit()  # ⚠️ Phải commit để lưu changes!

# Update
cursor.execute(
    "UPDATE users SET xp = xp + %s WHERE id = %s",
    (50, user_id)
)
conn.commit()

# Close
cursor.close()
conn.close()
```

**Lưu ý quan trọng**:
- Luôn dùng `%s` placeholders, KHÔNG concatenate string (tránh SQL injection)
- Phải `commit()` sau INSERT/UPDATE/DELETE
- Phải `close()` cursor và connection

### 4. REST API với Flask

Flask Blueprint để organize routes:

```python
from flask import Blueprint, request, jsonify

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user), 200

@user_bp.route('/api/profile/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    data = request.json
    success = UserService.update_profile(user_id, data)
    if success:
        return jsonify({'message': 'Updated'}), 200
    else:
        return jsonify({'error': 'Failed'}), 500
```

**HTTP Methods**:
- **GET**: Lấy dữ liệu (không thay đổi database)
- **POST**: Tạo mới (login, signup)
- **PUT**: Cập nhật toàn bộ
- **PATCH**: Cập nhật một phần
- **DELETE**: Xóa

**Status Codes**:
- **200 OK**: Thành công
- **201 Created**: Tạo mới thành công
- **400 Bad Request**: Dữ liệu không hợp lệ
- **401 Unauthorized**: Chưa đăng nhập
- **404 Not Found**: Không tìm thấy
- **500 Internal Server Error**: Lỗi server

### 5. Password Hashing

KHÔNG BAO GIỜ lưu plaintext password:

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Khi đăng ký
password = 'mypassword123'
password_hash = generate_password_hash(password, method='scrypt')
# → 'scrypt:32768:8:1$...'

# Lưu vào DB
cursor.execute(
    "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
    (username, password_hash)
)

# Khi đăng nhập
input_password = 'mypassword123'
cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
result = cursor.fetchone()

if check_password_hash(result['password_hash'], input_password):
    print("Login successful")
else:
    print("Wrong password")
```

**Scrypt**: Thuật toán hash chống brute-force attacks.

---

## 📂 Files Bạn Phụ Trách

### 1. `backend/services/user_service.py` (240 dòng)

**Vai trò**: CRUD operations cho users

**Các hàm chính**:

#### `get_user_by_id(user_id)`
```python
@staticmethod
def get_user_by_id(user_id):
    query = """
        SELECT u.*, r.name as rank_name, r.color as rank_color
        FROM users u
        LEFT JOIN ranks r ON u.rank_id = r.id
        WHERE u.id = %s
    """
    user = DatabaseQuery.execute_query(query, (user_id,), fetch_one=True)
    
    if user:
        # Enrich with tier info
        tier_info = RankService.get_tier_info(user['level'])
        user['tier_name'] = tier_info['name']
        user['tier_color'] = tier_info['color']
    
    return user
```

#### `get_user_by_username(username)`
Tương tự `get_user_by_id` nhưng WHERE username.

#### `create_user(username, password, display_name, email)`
```python
@staticmethod
def create_user(username, password, display_name, email):
    # Kiểm tra username đã tồn tại chưa
    existing = DatabaseQuery.execute_query(
        "SELECT id FROM users WHERE username = %s",
        (username,),
        fetch_one=True
    )
    if existing:
        raise ValueError("Username already exists")
    
    # Hash password
    password_hash = generate_password_hash(password, method='scrypt')
    
    # Insert
    query = """
        INSERT INTO users (username, password_hash, display_name, email, level, xp, rank_score, rank_id)
        VALUES (%s, %s, %s, %s, 1, 0, 0, 1)
    """
    DatabaseQuery.execute_update(query, (username, password_hash, display_name, email))
    
    # Lấy user vừa tạo
    return UserService.get_user_by_username(username)
```

#### `authenticate(username, password)`
```python
@staticmethod
def authenticate(username, password):
    user = UserService.get_user_by_username(username)
    if not user:
        return None
    
    if check_password_hash(user['password_hash'], password):
        return user
    else:
        return None
```

#### `update_profile(user_id, data)`
```python
@staticmethod
def update_profile(user_id, data):
    fields = []
    values = []
    
    # Chỉ update các field được gửi lên
    allowed_fields = ['display_name', 'full_name', 'bio', 'avatar_url', 'date_of_birth']
    for field in allowed_fields:
        if field in data:
            fields.append(f"{field} = %s")
            values.append(data[field])
    
    if not fields:
        return True
    
    values.append(user_id)
    query = f"UPDATE users SET {', '.join(fields)} WHERE id = %s"
    DatabaseQuery.execute_update(query, tuple(values))
    return True
```

**Vị trí**: `c:\xampp\htdocs\Caro\backend\services\user_service.py`

### 2. `backend/services/rank_service.py` (176 dòng)

**Vai trò**: Logic tính toán ranking

**Các hàm chính**:

####  `get_level_from_score(xp)`
```python
@staticmethod
def get_level_from_score(xp):
    if xp < 0:
        return 1
    
    query = """
        SELECT level
        FROM game_levels
        WHERE required_score <= %s
        ORDER BY level DESC
        LIMIT 1
    """
    result = DatabaseQuery.execute_query(query, (xp,), fetch_one=True)
    return result['level'] if result else 1
```

#### `get_tier_info(level)`
```python
@staticmethod
def get_tier_info(level):
    query = """
        SELECT name, color, description
        FROM tiers
        WHERE %s BETWEEN min_level AND max_level
        LIMIT 1
    """
    result = DatabaseQuery.execute_query(query, (level,), fetch_one=True)
    
    if not result:
        return {'name': 'Tân Thủ', 'color': '#9E9E9E', 'description': 'Người mới'}
    
    return result
```

#### `update_rank(user_id, rank_points_delta, xp_delta)`
Hàm QUAN TRỌNG NHẤT!

```python
@staticmethod
def update_rank(user_id, rank_points_delta, xp_delta):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # 1. Lấy giá trị hiện tại
    cursor.execute("SELECT xp, level, rank_score FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    
    current_xp = user['xp']
    current_level = user['level']
    current_rank_score = user['rank_score']
    
    # 2. Tính giá trị mới
    new_xp = current_xp + xp_delta
    new_rank_score = max(0, current_rank_score + rank_points_delta)  # Không âm
    
    # 3. Tính new_rank_id từ rank_score
    new_rank_id = UserService.calculate_rank_id(new_rank_score)
    
    # 4. Tính new_level từ game_levels table
    cursor.execute(
        "SELECT level FROM game_levels WHERE required_score <= %s ORDER BY level DESC LIMIT 1",
        (new_xp,)
    )
    level_row = cursor.fetchone()
    new_level = level_row['level'] if level_row else 1
    
    # 5. Update database
    cursor.execute(
        "UPDATE users SET xp = %s, level = %s, rank_score = %s, rank_id = %s WHERE id = %s",
        (new_xp, new_level, new_rank_score, new_rank_id, user_id)
    )
    
    # 6. Nếu level thay đổi → log history
    if new_level != current_level:
        cursor.execute(
            "INSERT INTO user_levels_history (user_id, level, xp) VALUES (%s, %s, %s)",
            (user_id, new_level, new_xp)
        )
    
    conn.commit()
    cursor.close()
    conn.close()
    return True
```

**Vị trí**: `c:\xampp\htdocs\Caro\backend\services\rank_service.py`

### 3. `backend/services/match_service.py` (130 dòng)

**Vai trò**: Lưu và lấy match history

#### `save_match(player1_id, player2_id, winner_id, game_type, mode, moves, duration)`
```python
@staticmethod
def save_match(player1_id, player2_id, winner_id, game_type, mode, moves, duration):
    import json
    
    moves_json = json.dumps(moves)
    
    query = """
        INSERT INTO match_history (player1_id, player2_id, winner_id, game_type, mode, moves, duration)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    DatabaseQuery.execute_update(query, (
        player1_id,
        player2_id if player2_id != 'AI' else None,
        winner_id if winner_id != 'draw' else None,
        game_type,
        mode,
        moves_json,
        duration
    ))
```

#### `get_user_matches(user_id)`
```python
@staticmethod
def get_user_matches(user_id):
    query = """
        SELECT m.*,
               p1.display_name as player1_name,
               p2.display_name as player2_name,
               w.display_name as winner_name
        FROM match_history m
        LEFT JOIN users p1 ON m.player1_id = p1.id
        LEFT JOIN users p2 ON m.player2_id = p2.id
        LEFT JOIN users w ON m.winner_id = w.id
        WHERE m.player1_id = %s OR m.player2_id = %s
        ORDER BY m.created_at DESC
        LIMIT 100
    """
    return DatabaseQuery.execute_query(query, (user_id, user_id))
```

**Vị trí**: `c:\xampp\htdocs\Caro\backend\services\match_service.py`

### 4. `backend/services/leaderboard_service.py` (110 dòng)

**Vai trò**: Lấy top players

#### `get_top_players(limit=100)`
```python
@staticmethod
def get_top_players(limit=100):
    query = """
        SELECT u.id, u.username, u.display_name, u.level, u.xp, u.rank_score,
               r.name as rank_name, r.color as rank_color
        FROM users u
        LEFT JOIN ranks r ON u.rank_id = r.id
        ORDER BY u.rank_score DESC, u.xp DESC
        LIMIT %s
    """
    players = DatabaseQuery.execute_query(query, (limit,))
    
    # Enrich với tier info
    for player in players:
        tier_info = RankService.get_tier_info(player['level'])
        player['tier_name'] = tier_info['name']
        player['tier_color'] = tier_info['color']
    
    return players
```

**Vị trí**: `c:\xampp\htdocs\Caro\backend\services\leaderboard_service.py`

### 5. `backend/routes/auth.py` (60 dòng) - Login/Signup APIs

```python
@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Missing fields'}), 400
    
    user = UserService.authenticate(username, password)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    display_name = data.get('display_name', username)
    email = data.get('email')
    
    if not username or not password:
        return jsonify({'error': 'Missing fields'}), 400
    
    try:
        user = UserService.create_user(username, password, display_name, email)
        return jsonify(user), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
```

**Vị trí**: `c:\xampp\htdocs\Caro\backend\routes\auth.py`

### 6. `backend/routes/user.py` (170 dòng) - User APIs

```python
@user_bp.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user), 200

@user_bp.route('/api/profile/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    data = request.json
    success = UserService.update_profile(user_id, data)
    if success:
        return jsonify({'message': 'Profile updated'}), 200
    else:
        return jsonify({'error': 'Update failed'}), 500

@user_bp.route('/api/history/<int:user_id>', methods=['GET'])
def get_match_history(user_id):
    matches = MatchService.get_user_matches(user_id)
    return jsonify(matches), 200
```

**Vị trí**: `c:\xampp\htdocs\Caro\backend\routes\user.py`

---

## 🔄 Luồng Hoạt Động Chi Tiết

### A. Luồng Login

1. Frontend POST `/api/login` với `{username, password}`
2. `auth.py` gọi `UserService.authenticate(username, password)`
3. `UserService` query database lấy user
4. Check password bằng `check_password_hash`
5. Nếu đúng: return full user profile (với tier info enriched)
6. Nếu sai: return 401 Unauthorized

### B. Luồng Update Rank

**Sau mỗi trận ranked**:

```python
# In sockets/game.py → _handle_end_game()
if winner == player1_id:
    RankService.update_rank(player1_id, rank_points_delta=+25, xp_delta=+50)
    RankService.update_rank(player2_id, rank_points_delta=-10, xp_delta=+15)
elif winner == player2_id:
    RankService.update_rank(player2_id, rank_points_delta=+25, xp_delta=+50)
    RankService.update_rank(player1_id, rank_points_delta=-10, xp_delta=+15)
else:  # draw
    RankService.update_rank(player1_id, rank_points_delta=0, xp_delta=+15)
    RankService.update_rank(player2_id, rank_points_delta=0, xp_delta=+15)
```

**Trong `RankService.update_rank`**:
1. Lấy current XP, level, rank_score
2. Tính new XP, new rank_score
3. Query `game_levels` để tính new level từ new XP
4. Tính new rank_id từ rank_score
5. UPDATE users table
6. Nếu level thay đổi → INSERT vào `user_levels_history`

### C. Luồng Calculate Level từ XP

**Ví dụ**: User có XP = 12,500

```sql
SELECT level
FROM game_levels
WHERE required_score <= 12500
ORDER BY level DESC
LIMIT 1
```

→ Kết quả: level 126 (vì level 126 cần 12,500 XP, level 127 cần 12,700 XP)

**game_levels table**:
```
level | required_score
------|---------------
1     | 0
2     | 100
...   | ...
100   | 9,900
101   | 10,000
...   | ...
126   | 12,500
127   | 12,700
```

Logic: Tìm level cao nhất mà `required_score <= user_xp`.

---

## 📋 Bảng Các Hàm Quan Trọng

| Hàm | File | Tham số | Chức năng |
|-----|------|---------|-----------|
| `get_user_by_id` | user_service.py | user_id | Lấy user từ DB, enrich với tier info |
| `get_user_by_username` | user_service.py | username | Tương tự, dùng cho login |
| `create_user` | user_service.py | username, password, display_name, email | Tạo user mới, hash password |
| `authenticate` | user_service.py | username, password | Kiểm tra login |
| `update_profile` | user_service.py | user_id, data | Cập nhật profile |
| `calculate_rank_id` | user_service.py | rank_score | Tính rank_id từ rank_score (1-4) |
| `get_level_from_score` | rank_service.py | xp | Query game_levels để tính level |
| `get_tier_info` | rank_service.py | level | Query tiers table |
| `update_rank` | rank_service.py | user_id, rank_delta, xp_delta | Cập nhật XP, level, rank sau trận đấu |
| `save_match` | match_service.py | player1_id, player2_id, winner_id, ... | Lưu match history |
| `get_user_matches` | match_service.py | user_id | Lấy lịch sử trận đấu |
| `get_top_players` | leaderboard_service.py | limit | Top players theo rank_score |

---

## 🎤 Nội Dung Thuyết Trình

### 1. Giới Thiệu Vai Trò (1 phút)
"Em phụ trách phần **Database và Ranking System**, là nơi lưu trữ toàn bộ dữ liệu game. Bao gồm:
- Hệ thống user authentication với password hashing
- APIs RESTful cho frontend gọi
- Logic tính toán ranking phức tạp (500 levels, 10 tiers, 4 ranks)
- Lưu trữ match history"

### 2. Database Schema (2 phút)

**Demo ERD diagram hoặc table structure**:

"Database có 6 tables chính:

**1. users**: Lưu user info và ranking stats
- `xp`: Kinh nghiệm (chỉ tăng) → quyết định `level`
- `rank_score`: Điểm rank (có thể giảm) → quyết định `rank_id`
- `level`: 1-500
- `rank_id`: 1-4 (Bronze → Crystal)

**2. game_levels**: Bảng lookup cho 500 levels
- Mỗi level có `required_score` (XP cần thiết)
- VD: Level 100 cần 9,900 XP

**3. tiers**: 10 danh hiệu theo level
- Tân Thủ (1-50), Nhập Môn (51-100), ..., Chí Tôn (451-500)

**4. ranks**: 4 hạng theo rank_score
- Bronze (0-499), Silver (500-999), Gold (1000+), Crystal (2000+)

**5. match_history**: Lịch sử trận đấu
- Lưu moves dưới dạng JSON string
- VD: `[{r:0,c:0,player:1}, {r:1,c:1,player:2}, ...]`

**6. user_levels_history**: Log lịch sử lên cấp"

### 3. Ranking System Logic (2.5 phút)

"Hệ thống ranking có 2 hệ điểm song song:

**XP (Experience Points)**:
- Thắng ranked: +50 XP
- Thua ranked: +15 XP
- Chỉ tăng, không giảm
- Quyết định Level (1-500)

**Rank Points**:
- Thắng: +25 pts
- Thua: -10 pts
- Có thể giảm xuống 0
- Quyết định Rank (Bronze/Silver/Gold/Crystal)

**Cách tính Level từ XP**:
```sql
SELECT level FROM game_levels
WHERE required_score <= 12500
ORDER BY level DESC LIMIT 1
```
→ Tìm level cao nhất mà XP đủ điều kiện

**Khi nào cập nhật?**
Sau mỗi trận ranked, em gọi `RankService.update_rank()`:
1. Cộng/trừ XP và Rank Points
2. Tính lại Level từ game_levels table
3. Tính lại Rank ID từ rank_score
4. UPDATE users table
5. Nếu level up → log vào user_levels_history"

**Demo code**:
```python
RankService.update_rank(user_id, rank_points_delta=+25, xp_delta=+50)
```

### 4. Password Security (1 phút)

"Em dùng **Scrypt** để hash password:

```python
# Khi đăng ký
password_hash = generate_password_hash('mypassword123', method='scrypt')
# → 'scrypt:32768:8:1$AbC123...'

# Khi login
if check_password_hash(stored_hash, input_password):
    return user  # Đúng password
```

Scrypt là thuật toán chống brute-force - mất nhiều thời gian để hash → hacker không thể thử hàng triệu passwords."

### 5. RESTful APIs (1.5 phút)

"Em implement các API endpoints:

**Authentication**:
- `POST /api/login` - Đăng nhập
- `POST /api/signup` - Đăng ký

**User Management**:
- `GET /api/user/:id` - Lấy thông tin user
- `PUT /api/profile/:id` - Cập nhật profile
- `POST /api/change-password/:id` - Đổi password

**Match History**:
- `GET /api/history/:userId` - Lịch sử trận đấu
- `GET /api/match/:matchId` - Chi tiết 1 trận (cho replay)

**Leaderboard**:
- `GET /api/leaderboard` - Top 100 players

Tất cả đều return JSON và có status codes chuẩn (200, 404, 500...)"

### 6. Tổng Kết (0.5 phút)

"Phần Database đảm bảo dữ liệu được lưu an toàn và chính xác. Ranking system phức tạp với 500 levels + 10 tiers + 4 ranks tạo motivation cho người chơi."

---

## 💡 Tips Học Hiệu Quả

1. **Chạy SQL queries trực tiếp trong MySQL**
   - Mở phpMyAdmin
   - Thử các queries SELECT, UPDATE
   - Xem kết quả thay đổi

2. **Test APIs với Postman**
   - Gửi POST /api/login với username/password
   - Xem response
   - Trace code từ route → service → database

3. **Hiểu flow update_rank**
   - Đọc code từ đầu đến cuối
   - Vẽ diagram: XP → Level, Rank Points → Rank ID
   - Test với các case: thắng, thua, level up

4. **Học SQL cơ bản**
   - W3Schools SQL Tutorial
   - Thực hành với các bài tập

Chúc bạn học tốt! Database là nền tảng của mọi ứng dụng! 💾
