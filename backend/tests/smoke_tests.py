"""
Ad-hoc smoke tests for AI decisions and matchmaking flows.

These checks give fast feedback that the advanced AI and instant-practice
matchmaking behave as expected without launching the full frontend.
"""
import os
import random
import sys
from typing import List, Tuple

# Ensure project root (backend/) is on sys.path when running as a script
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app  # noqa: E402
from game.ai import AIPlayer  # noqa: E402
from game.engine import GameEngine  # noqa: E402
from services.user_service import UserService  # noqa: E402
from sockets import matchmaking as matchmaking_module  # noqa: E402


def _assert_move_in_board(move, board, label: str):
    assert isinstance(move, tuple) and len(move) == 2, f"{label}: invalid move type {move}"
    r, c = move
    assert 0 <= r < len(board) and 0 <= c < len(board[0]), f"{label}: move {move} outside board"
    assert board[r][c] == 0, f"{label}: move {move} not empty"


def run_ai_checks() -> List[Tuple[str, Tuple[int, int]]]:
    """Run deterministic AI behavior checks across difficulties."""
    results = []

    # Tic-Tac-Toe Easy
    board = GameEngine.create_board('tic-tac-toe')
    board[0][0] = 1
    random.seed(0)
    move = AIPlayer.get_ai_move(board, 'tic-tac-toe', 'easy')
    _assert_move_in_board(move, board, 'TTT Easy')
    results.append(('Tic-Tac-Toe Easy', move))

    # Tic-Tac-Toe Medium (force optimal path)
    board = [
        [2, 2, 0],
        [1, 1, 0],
        [0, 0, 0]
    ]
    original_random = random.random
    random.random = lambda: 0.9
    move = AIPlayer.get_ai_move(board, 'tic-tac-toe', 'medium')
    random.random = original_random
    assert move == (0, 2), f"TTT Medium should finish winning row, got {move}"
    results.append(('Tic-Tac-Toe Medium', move))

    # Tic-Tac-Toe Hard (defensive block)
    board = [
        [1, 1, 0],
        [0, 2, 0],
        [0, 0, 2]
    ]
    move = AIPlayer.get_ai_move(board, 'tic-tac-toe', 'hard')
    assert move == (0, 2), f"TTT Hard should block top row, got {move}"
    results.append(('Tic-Tac-Toe Hard', move))

    # Caro Easy plays near pieces
    board = GameEngine.create_board('caro')
    existing = [(7, 7), (8, 8)]
    for r, c in existing:
        board[r][c] = 1 if (r, c) == (7, 7) else 2
    random.seed(1)
    move = AIPlayer.get_ai_move(board, 'caro', 'easy')
    _assert_move_in_board(move, board, 'Caro Easy')
    assert any(abs(move[0] - r) <= 2 and abs(move[1] - c) <= 2 for r, c in existing), \
        f"Caro Easy move {move} too far from pieces"
    results.append(('Caro Easy', move))

    # Caro Medium takes immediate win
    board = GameEngine.create_board('caro')
    row = 5
    for col in range(6, 10):
        board[row][col] = 2
    board[row][5] = 1  # block left side so only right end is open
    move = AIPlayer.get_ai_move(board, 'caro', 'medium')
    assert move == (row, 10), f"Caro Medium should finish open four, got {move}"
    results.append(('Caro Medium', move))

    # Caro Hard blocks opponent fork
    board = GameEngine.create_board('caro')
    row = 10
    for col in range(0, 4):
        board[row][col] = 1
    move = AIPlayer.get_ai_move(board, 'caro', 'hard')
    assert move == (row, 4), f"Caro Hard should block opponent threat, got {move}"
    results.append(('Caro Hard', move))

    return results


def _reset_matchmaking_state():
    """Ensure matchmaking module starts from a clean slate."""
    for key in matchmaking_module.matchmaking_queue:
        matchmaking_module.matchmaking_queue[key] = []
    matchmaking_module.games.clear()


def run_practice_flow(socketio, app):
    """Ensure practice mode emits match_found immediately without queueing."""
    _reset_matchmaking_state()
    client = socketio.test_client(app)
    payload = {
        'userId': 99,
        'type': 'tic-tac-toe',
        'mode': 'practice',
        'difficulty': 'medium'
    }
    client.emit('join_matchmaking', payload)
    received = client.get_received()
    match_events = [evt for evt in received if evt['name'] == 'match_found']
    assert match_events, "Practice flow did not emit match_found"
    data = match_events[0]['args'][0]
    assert data['mode'] == 'practice', "Practice flow returned wrong mode"
    assert data['difficulty'] == 'medium', "Practice flow missing difficulty"
    assert data['playerNumber'] == 1, "Practice flow should assign player 1"
    return data


def run_ranked_flow(socketio, app):
    """Ensure two ranked players are matched via the queue."""
    _reset_matchmaking_state()
    client1 = socketio.test_client(app)
    client2 = socketio.test_client(app)

    payload1 = {'userId': 1, 'type': 'tic-tac-toe', 'mode': 'ranked'}
    payload2 = {'userId': 2, 'type': 'tic-tac-toe', 'mode': 'ranked'}

    client1.emit('join_matchmaking', payload1)
    client2.emit('join_matchmaking', payload2)

    received1 = client1.get_received()
    received2 = client2.get_received()

    match1 = next((evt for evt in received1 if evt['name'] == 'match_found'), None)
    match2 = next((evt for evt in received2 if evt['name'] == 'match_found'), None)
    assert match1 and match2, "Ranked flow did not match both players"

    room1 = match1['args'][0]['roomId']
    room2 = match2['args'][0]['roomId']
    assert room1 == room2, "Players were not matched into same room"
    assert match1['args'][0]['mode'] == 'ranked'
    assert match2['args'][0]['mode'] == 'ranked'
    return room1


def main():
    app, socketio = create_app()

    # Patch user service to avoid DB dependency during smoke tests
    UserService.get_user_by_id = staticmethod(lambda user_id: {
        'id': user_id,
        'display_name': f'User {user_id}'
    })

    ai_results = run_ai_checks()
    practice_result = run_practice_flow(socketio, app)
    ranked_room = run_ranked_flow(socketio, app)

    print("AI Checks:")
    for label, move in ai_results:
        print(f" - {label}: {move}")

    print(f"Practice Flow: matched room {practice_result['roomId']} vs {practice_result['opponent']['display_name']}")
    print(f"Ranked Flow: matched players into room {ranked_room}")


if __name__ == "__main__":
    main()

