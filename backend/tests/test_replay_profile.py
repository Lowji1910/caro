import unittest
import sys
import os
import json

# Add backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from database.db import DatabaseQuery
from services.user_service import UserService
from services.match_service import MatchService

class TestReplayProfile(unittest.TestCase):
    def setUp(self):
        self.app, self.socketio = create_app()
        self.client = self.app.test_client()
        
        # Create test users
        self.user1 = UserService.create_user('test_p1', 'password', 'Player 1', 'p1@test.com')
        self.user2 = UserService.create_user('test_p2', 'password', 'Player 2', 'p2@test.com')
        
        if not self.user1:
            self.user1 = UserService.get_user_by_username('test_p1')
        if not self.user2:
            self.user2 = UserService.get_user_by_username('test_p2')

    def test_public_profile(self):
        print("\n--- Testing Public Profile API ---")
        res = self.client.get(f'/api/public/{self.user1["id"]}')
        self.assertEqual(res.status_code, 200)
        data = res.json
        
        print(f"Public Profile Data: {data}")
        self.assertIn('display_name', data)
        self.assertIn('rank_score', data)
        self.assertNotIn('password', data)
        self.assertNotIn('email', data)
        print("Public Profile verified: No sensitive data exposed.")

    def test_match_replay(self):
        print("\n--- Testing Match Replay API ---")
        # Create a dummy match
        moves = [{'r': 0, 'c': 0, 'player': 1}, {'r': 0, 'c': 1, 'player': 2}]
        match_id = MatchService.save_match(
            self.user1['id'], 
            self.user2['id'], 
            self.user1['id'], 
            'tic-tac-toe', 
            'ranked'
        )
        
        # Manually update moves
        moves_json = json.dumps(moves)
        query = "UPDATE match_history SET moves = %s WHERE id = %s"
        DatabaseQuery.execute_update(query, (moves_json, match_id))
        
        # Fetch match details
        res = self.client.get(f'/api/match/{match_id}')
        self.assertEqual(res.status_code, 200)
        data = res.json
        
        print(f"Match Details: {data}")
        self.assertEqual(data['id'], match_id)
        self.assertEqual(data['p1_name'], 'Player 1')
        self.assertEqual(data['p2_name'], 'Player 2')
        
        # Verify moves
        fetched_moves = data['moves']
        if isinstance(fetched_moves, str):
            fetched_moves = json.loads(fetched_moves)
            
        self.assertEqual(len(fetched_moves), 2)
        self.assertEqual(fetched_moves[0]['r'], 0)
        self.assertEqual(fetched_moves[0]['c'], 0)
        print("Match Replay verified: Moves returned correctly.")

    def tearDown(self):
        # Clean up (optional, or use a test DB)
        pass

if __name__ == '__main__':
    unittest.main()
