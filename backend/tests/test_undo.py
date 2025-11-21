import unittest
import time
import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from flask_socketio import SocketIOTestClient

class TestUndoFeature(unittest.TestCase):
    def setUp(self):
        self.app, self.socketio = create_app()
        self.client1 = self.socketio.test_client(self.app)
        self.client2 = self.socketio.test_client(self.app)
        
    def test_undo_flow(self):
        # 1. Setup match
        print("\n--- Starting Undo Flow Test ---")
        
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
        print("Player 1 making a move at (0, 0)...")
        self.client1.emit('make_move', {'roomId': room_id, 'r': 0, 'c': 0, 'player': 1})
        
        # Verify move applied
        received2 = self.client2.get_received()
        update_event = next((e for e in received2 if e['name'] == 'game_update'), None)
        self.assertTrue(update_event, "Game update not received")
        board = update_event['args'][0]['board']
        self.assertEqual(board[0][0], 1, "Move not applied correctly")
        
        # 3. Player 1 requests undo
        print("Player 1 requesting undo...")
        self.client1.emit('request_undo', {'roomId': room_id})
        
        # Verify Player 2 receives request
        received2 = self.client2.get_received()
        undo_req_event = next((e for e in received2 if e['name'] == 'undo_requested'), None)
        self.assertTrue(undo_req_event, "Undo request not received by opponent")
        print("Player 2 received undo request.")
        
        # Clear client1 events to avoid reading the previous game_update
        self.client1.get_received()

        # 4. Player 2 accepts undo
        print("Player 2 accepting undo...")
        self.client2.emit('resolve_undo', {'roomId': room_id, 'accept': True})
        
        # Verify undo applied (Game Update)
        received1 = self.client1.get_received()
        undo_update_event = next((e for e in received1 if e['name'] == 'game_update'), None)
        self.assertTrue(undo_update_event, "Game update after undo not received")
        
        new_board = undo_update_event['args'][0]['board']
        self.assertEqual(new_board[0][0], 0, "Cell (0,0) should be empty after undo")
        self.assertEqual(undo_update_event['args'][0]['currentPlayer'], 1, "Turn should revert to Player 1")
        print("Undo successful! Board reverted and turn restored.")

if __name__ == '__main__':
    unittest.main()
