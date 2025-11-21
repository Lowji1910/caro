import unittest
import time
import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from flask_socketio import SocketIOTestClient
from unittest.mock import patch

class TestTimeoutFeature(unittest.TestCase):
    def setUp(self):
        # Mock services to avoid DB calls
        self.rank_patcher = patch('sockets.game.RankService')
        self.match_patcher = patch('sockets.game.MatchService')
        self.mock_rank = self.rank_patcher.start()
        self.mock_match = self.match_patcher.start()
        
        self.app, self.socketio = create_app()
        self.client1 = self.socketio.test_client(self.app)
        self.client2 = self.socketio.test_client(self.app)

    def tearDown(self):
        self.rank_patcher.stop()
        self.match_patcher.stop()
        
    def test_timeout_flow(self):
        # 1. Setup match
        print("\n--- Starting Timeout Flow Test ---")
        
        # Join matchmaking
        self.client1.emit('join_matchmaking', {'userId': 1, 'type': 'tic-tac-toe', 'mode': 'ranked'})
        self.client2.emit('join_matchmaking', {'userId': 2, 'type': 'tic-tac-toe', 'mode': 'ranked'})
        
        # Get room ID
        received1 = self.client1.get_received()
        match_event = next((e for e in received1 if e['name'] == 'match_found'), None)
        self.assertTrue(match_event, "Match not found")
        room_id = match_event['args'][0]['roomId']
        print(f"Match created in room: {room_id}")
        
        # 2. Player 1 makes a move
        print("Player 1 making a move...")
        self.client1.emit('make_move', {'roomId': room_id, 'r': 0, 'c': 0, 'player': 1})
        
        # Verify move applied
        received2 = self.client2.get_received()
        update_event = next((e for e in received2 if e['name'] == 'game_update'), None)
        self.assertTrue(update_event, "Game update not received")
        
        # Clear client1 events from the move
        self.client1.get_received()
        
        # 3. Simulate Timeout
        # It is now Player 2's turn.
        # If Player 2 runs out of time, Player 1 (waiting) claims timeout.
        print("Simulating timeout for Player 2...")
        self.client1.emit('claim_timeout', {'roomId': room_id})
        
        # 4. Verify Game End
        time.sleep(0.5)
        received1 = self.client1.get_received()
        print(f"Received events: {received1}")
        end_event = next((e for e in received1 if e['name'] == 'game_update'), None)
        self.assertTrue(end_event, "Game end update not received")
        
        data = end_event['args'][0]
        self.assertEqual(data['currentPlayer'], 0, "Game should be over (currentPlayer 0)")
        self.assertEqual(data['winner'], 1, "Player 1 should be the winner")
        print("Timeout successful! Player 1 wins.")

if __name__ == '__main__':
    unittest.main()
