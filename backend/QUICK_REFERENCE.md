# Backend Quick Reference Guide

## File Locations

### Configuration
- **config.py** - All settings and constants

### Database
- **database/db.py** - Database operations
  - `DatabaseConnection.get_connection()` - Get DB connection
  - `DatabaseQuery.execute_query()` - SELECT queries
  - `DatabaseQuery.execute_update()` - INSERT/UPDATE/DELETE
  - `DatabaseQuery.execute_transaction()` - Multi-operation

### Services (Business Logic)
- **services/user_service.py**
  - `authenticate(username, password)` - Login
  - `create_user(username, password, display_name)` - Register
  - `get_user_by_id(user_id)` - Get user
  - `update_profile(user_id, **kwargs)` - Update profile
  - `change_password(user_id, old_password, new_password)` - Change password

- **services/rank_service.py**
  - `calculate_user_level(rank_score)` - Get level
  - `update_rank(user_id, points)` - Update rank
  - `log_level_change(user_id, level, rank_score)` - Log change
  - `update_rank_batch(updates)` - Batch update

- **services/match_service.py**
  - `save_match(player1_id, player2_id, winner_id, game_type, mode)` - Save match
  - `get_user_match_history(user_id, limit=20)` - Get history
  - `get_match_stats(user_id)` - Get stats

- **services/leaderboard_service.py**
  - `get_leaderboard(limit=10)` - Get top players
  - `get_user_rank(user_id)` - Get rank position
  - `get_nearby_players(user_id, range_size=5)` - Get nearby

### Game Logic
- **game/engine.py**
  - `create_board(game_type)` - Create board
  - `check_winner(board, game_type, last_move)` - Check winner
  - `is_valid_move(board, r, c)` - Validate move
  - `apply_move(board, r, c, player)` - Apply move

- **game/ai.py**
  - `get_ai_move(board, game_type, difficulty)` - Get AI move
  - `_get_tictactoe_move(board, difficulty)` - Tic-Tac-Toe AI
  - `_get_caro_move(board, difficulty)` - Caro AI
  - `_find_caro_threat(board, player, count)` - Find threat

### API Routes
- **routes/auth.py**
  - `POST /api/login` - Login
  - `POST /api/signup` - Register

- **routes/user.py**
  - `GET /api/user/<id>` - Get profile
  - `PUT /api/profile/<id>` - Update profile
  - `POST /api/change-password/<id>` - Change password
  - `GET /api/history/<id>` - Match history
  - `GET /api/stats/<id>` - Statistics

- **routes/leaderboard.py**
  - `GET /api/leaderboard` - Top players
  - `GET /api/rank/<id>` - User rank
  - `GET /api/nearby/<id>` - Nearby players

### WebSocket Handlers
- **sockets/matchmaking.py**
  - `join_matchmaking` - Join queue
  - `_handle_practice_mode()` - Practice setup
  - `_handle_ranked_mode()` - Ranked matching

- **sockets/game.py**
  - `connect` - Client connect
  - `make_move` - Process move
  - `send_chat` - Chat message
  - `_handle_end_game()` - End game logic
  - `_handle_ai_move()` - AI move

### Main Application
- **app.py** - Flask initialization
  - `create_app()` - Create Flask app
  - `if __name__ == '__main__'` - Run server

---

## Common Tasks

### Add a New API Endpoint

1. Create service method in `services/`
2. Create route in `routes/`
3. Register blueprint in `app.py`

Example:
```python
# services/example_service.py
class ExampleService:
    @staticmethod
    def get_data():
        return {"data": "value"}

# routes/example.py
from flask import Blueprint
from services.example_service import ExampleService

example_bp = Blueprint('example', __name__, url_prefix='/api')

@example_bp.route('/example', methods=['GET'])
def get_example():
    data = ExampleService.get_data()
    return jsonify(data)

# app.py
from routes.example import example_bp
app.register_blueprint(example_bp)
```

### Add a New Game Type

1. Add config in `config.py`:
```python
GAME_CONFIG = {
    'new-game': {
        'rows': 10,
        'cols': 10,
        'win_length': 4
    }
}
```

2. Add AI logic in `game/ai.py` if needed

### Update Ranking Logic

Edit `services/rank_service.py`:
```python
class RankService:
    @staticmethod
    def update_rank(user_id, points):
        # Modify here
```

### Add Database Query

Use `database/db.py`:
```python
from database.db import DatabaseQuery

result = DatabaseQuery.execute_query(
    "SELECT * FROM users WHERE id = %s",
    (user_id,),
    fetch_one=True
)
```

### Modify Configuration

Edit `config.py`:
```python
RANKING_CONFIG = {
    'level_up_score': 100,  # Modify here
    'max_level': 500,
    'win_points': 25,
    'loss_points': -10
}
```

---

## API Examples

### Login
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"player1","password":"password123"}'
```

### Get User
```bash
curl http://localhost:5000/api/user/1
```

### Get Leaderboard
```bash
curl http://localhost:5000/api/leaderboard?limit=10
```

### Update Profile
```bash
curl -X PUT http://localhost:5000/api/profile/1 \
  -H "Content-Type: application/json" \
  -d '{"display_name":"New Name","bio":"New bio"}'
```

---

## WebSocket Examples

### Join Matchmaking
```javascript
socket.emit('join_matchmaking', {
  userId: 1,
  type: 'tic-tac-toe',
  mode: 'ranked'
});
```

### Make Move
```javascript
socket.emit('make_move', {
  roomId: 'room-id',
  r: 0,
  c: 1,
  player: 1
});
```

### Send Chat
```javascript
socket.emit('send_chat', {
  roomId: 'room-id',
  message: 'Hello!',
  sender: 'Player Name'
});
```

---

## Database Tables

### users
```sql
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(255) UNIQUE,
  password VARCHAR(255),
  display_name VARCHAR(255),
  full_name VARCHAR(255),
  date_of_birth DATE,
  bio TEXT,
  avatar_url VARCHAR(255),
  rank_score INT DEFAULT 0,
  rank_level VARCHAR(50) DEFAULT 'Bronze',
  user_level INT DEFAULT 1,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### match_history
```sql
CREATE TABLE match_history (
  id INT PRIMARY KEY AUTO_INCREMENT,
  player1_id INT,
  player2_id INT,
  winner_id INT,
  game_type VARCHAR(50),
  mode VARCHAR(50),
  played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (player1_id) REFERENCES users(id),
  FOREIGN KEY (player2_id) REFERENCES users(id),
  FOREIGN KEY (winner_id) REFERENCES users(id)
);
```

### user_levels_history
```sql
CREATE TABLE user_levels_history (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT,
  level INT,
  rank_score INT,
  changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## Environment Variables

Create `.env` file in backend directory:
```
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_NAME=tic_tac_toe_db
FRONTEND_ORIGIN=http://localhost:3000
DEBUG=False
HOST=0.0.0.0
PORT=5000
SECRET_KEY=secret!
```

---

## Debugging Tips

### Check Database Connection
```python
from database.db import DatabaseConnection
conn = DatabaseConnection.get_connection()
print("Connected!" if conn else "Failed!")
```

### Test Service
```python
from services.user_service import UserService
user = UserService.get_user_by_id(1)
print(user)
```

### Check Configuration
```python
import config
print(config.DB_CONFIG)
print(config.GAME_CONFIG)
```

---

## Performance Tips

1. **Use execute_transaction()** for multiple operations
2. **Cache leaderboard** with Redis
3. **Add connection pooling** for database
4. **Implement rate limiting** on routes
5. **Add logging** for debugging

---

## Security Checklist

- ✅ All queries are parameterized (SQL injection safe)
- ✅ Input validation on routes
- ✅ Error messages don't expose sensitive data
- ✅ CORS configured properly
- ⚠️ TODO: Add JWT authentication
- ⚠️ TODO: Hash passwords (currently plain text)
- ⚠️ TODO: Add rate limiting
- ⚠️ TODO: Add input sanitization

---

## Useful Commands

### Start Server
```bash
cd backend
python app.py
```

### Check Syntax
```bash
python -m py_compile app.py
```

### Run Tests (when added)
```bash
pytest tests/
```

### Format Code
```bash
black .
```

### Check Code Quality
```bash
pylint *.py
```

---

## Documentation Files

- **README.md** - Detailed documentation
- **MIGRATION_GUIDE.md** - Migration from old code
- **REFACTORING_SUMMARY.md** - Complete summary
- **QUICK_REFERENCE.md** - This file
