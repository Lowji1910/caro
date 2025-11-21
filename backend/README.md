# Ranked Arena Backend

## Overview
Well-organized, modular Flask + SocketIO backend for the Ranked Arena game server. All game logic, user management, and real-time features are cleanly separated into logical modules.

## Project Structure

```
backend/
├── app.py                          # Flask app initialization
├── config.py                       # Configuration & constants
├── requirements.txt                # Python dependencies
│
├── database/
│   ├── __init__.py
│   └── db.py                       # Database connection & query utilities
│
├── services/                       # Business logic layer
│   ├── __init__.py
│   ├── user_service.py             # User authentication & profile management
│   ├── rank_service.py             # Ranking & level calculations
│   ├── match_service.py            # Match history & statistics
│   └── leaderboard_service.py      # Leaderboard queries
│
├── game/                           # Game logic
│   ├── __init__.py
│   ├── engine.py                   # Board creation, winner checking
│   └── ai.py                       # AI move generation
│
├── routes/                         # API endpoints (Flask blueprints)
│   ├── __init__.py
│   ├── auth.py                     # /api/login, /api/signup
│   ├── user.py                     # /api/user, /api/profile, /api/history
│   └── leaderboard.py              # /api/leaderboard, /api/rank
│
└── sockets/                        # WebSocket event handlers
    ├── __init__.py
    ├── matchmaking.py              # Queue management, match finding
    └── game.py                     # Game moves, AI, end game handling
```

## Module Descriptions

### `config.py`
Centralized configuration management:
- Database connection settings
- Game configurations (board sizes, win conditions)
- Ranking system constants
- CORS and Flask settings

### `database/db.py`
Database abstraction layer:
- `DatabaseConnection`: Connection management
- `DatabaseQuery`: Query execution utilities
  - `execute_query()`: SELECT queries
  - `execute_update()`: INSERT/UPDATE/DELETE
  - `execute_transaction()`: Multi-operation transactions

### `services/`
Business logic layer - reusable across routes and sockets:

**user_service.py**
- `authenticate()`: Login verification
- `get_user_by_id()`, `get_user_by_username()`
- `create_user()`: Registration
- `update_profile()`: Profile updates
- `change_password()`: Password management

**rank_service.py**
- `calculate_user_level()`: Level from rank score
- `update_rank()`: Update score and level
- `log_level_change()`: History tracking
- `update_rank_batch()`: Batch updates

**match_service.py**
- `save_match()`: Record completed match
- `get_user_match_history()`: Match records
- `get_match_stats()`: Win/loss/draw counts

**leaderboard_service.py**
- `get_leaderboard()`: Top players
- `get_user_rank()`: Player's rank position
- `get_nearby_players()`: Players near user's rank

### `game/`
Game logic modules:

**engine.py**
- `create_board()`: Initialize empty board
- `check_winner()`: Detect win/draw
- `is_valid_move()`: Move validation
- `apply_move()`: Place piece on board

**ai.py**
- `get_ai_move()`: AI move selection
- `_get_tictactoe_move()`: Minimax algorithm
- `_get_caro_move()`: Greedy heuristic
- `_find_caro_threat()`: Threat detection

### `routes/`
Flask blueprints for REST API:

**auth.py**
- `POST /api/login`: User authentication
- `POST /api/signup`: User registration

**user.py**
- `GET /api/user/<id>`: Get user profile
- `PUT /api/profile/<id>`: Update profile
- `POST /api/change-password/<id>`: Change password
- `GET /api/history/<id>`: Match history
- `GET /api/stats/<id>`: User statistics

**leaderboard.py**
- `GET /api/leaderboard`: Global leaderboard
- `GET /api/rank/<id>`: User's rank position
- `GET /api/nearby/<id>`: Nearby players

### `sockets/`
WebSocket event handlers:

**matchmaking.py**
- `join_matchmaking`: Queue management
- `_handle_practice_mode()`: AI opponent setup
- `_handle_ranked_mode()`: Player matching

**game.py**
- `connect`: Client connection
- `make_move`: Move processing & validation
- `send_chat`: Chat messaging
- `_handle_end_game()`: Rank updates & history
- `_handle_ai_move()`: AI move execution

### `app.py`
Main application entry point:
- Flask app creation
- CORS configuration
- SocketIO setup
- Blueprint registration
- Socket handler registration

## Key Design Patterns

### 1. Separation of Concerns
- **Database Layer**: Handles all DB operations
- **Service Layer**: Contains business logic
- **Route Layer**: Handles HTTP requests
- **Socket Layer**: Handles WebSocket events
- **Game Logic**: Isolated game rules

### 2. Reusability
Services are used by both routes and sockets, eliminating code duplication.

### 3. Configuration Management
All constants and settings in `config.py` for easy modification.

### 4. Error Handling
Consistent error responses across all endpoints.

### 5. Scalability
Easy to add new routes, services, or game types without modifying existing code.

## Running the Application

### Prerequisites
```bash
pip install -r requirements.txt
```

### Start the Server
```bash
python app.py
```

Server runs on `http://0.0.0.0:5000` by default.

### Environment Variables
Create a `.env` file in the backend directory:
```
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_NAME=tic_tac_toe_db
FRONTEND_ORIGIN=http://localhost:3000
DEBUG=False
HOST=0.0.0.0
PORT=5000
```

## API Endpoints

### Authentication
- `POST /api/login` - Login
- `POST /api/signup` - Register

### User Management
- `GET /api/user/<id>` - Get profile
- `PUT /api/profile/<id>` - Update profile
- `POST /api/change-password/<id>` - Change password
- `GET /api/history/<id>` - Match history
- `GET /api/stats/<id>` - Statistics

### Leaderboard
- `GET /api/leaderboard` - Top players
- `GET /api/rank/<id>` - User's rank
- `GET /api/nearby/<id>` - Nearby players

### WebSocket Events
- `join_matchmaking` - Join game queue
- `make_move` - Play a move
- `send_chat` - Send message

## Database Schema Requirements

The application expects the following tables:
- `users` - User accounts
- `match_history` - Completed matches
- `user_levels_history` - Level change tracking

## Future Enhancements

1. **Authentication**: Add JWT tokens for security
2. **Caching**: Redis for leaderboard caching
3. **Logging**: Structured logging system
4. **Testing**: Unit and integration tests
5. **Database**: Connection pooling with SQLAlchemy
6. **API Documentation**: Swagger/OpenAPI
7. **Rate Limiting**: Prevent abuse
8. **Game Types**: Easy to add new games

## Maintenance Notes

- All database queries are parameterized to prevent SQL injection
- Services handle their own error cases
- Routes validate input before passing to services
- Socket handlers use services for business logic
- Configuration is centralized for easy updates

## Code Quality

- **DRY Principle**: No code duplication
- **Single Responsibility**: Each module has one job
- **Consistent Naming**: Clear, descriptive names
- **Documentation**: Docstrings on all functions
- **Error Handling**: Proper exception management
