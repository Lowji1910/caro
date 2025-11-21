"""
Match service: Game history, match results, winner determination.
"""
from database.db import DatabaseQuery


class MatchService:
    """Handles match history and game result recording."""
    
    @staticmethod
    def save_match(player1_id, player2_id, winner_id, game_type, mode, moves=None):
        """
        Save a completed match to history.
        
        Args:
            player1_id: ID of player 1
            player2_id: ID of player 2
            winner_id: ID of winner (None for draw)
            game_type: 'tic-tac-toe' or 'caro'
            mode: 'ranked' or 'practice'
            moves: List of move dicts (optional)
        
        Returns:
            Match ID if successful, None otherwise
        """
        import json
        moves_json = json.dumps(moves) if moves else None
        query = """
            INSERT INTO match_history (player1_id, player2_id, winner_id, game_type, mode, moves)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return DatabaseQuery.execute_update(query, (player1_id, player2_id, winner_id, game_type, mode, moves_json))
    
    @staticmethod
    def get_user_match_history(user_id, limit=20):
        """
        Get match history for a user.
        
        Args:
            user_id: User's ID
            limit: Maximum number of matches to return
        
        Returns:
            List of match records
        """
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
            ORDER BY m.played_at DESC LIMIT %s
        """
        return DatabaseQuery.execute_query(
            query,
            (user_id, user_id, user_id, user_id, limit),
            fetch_all=True
        ) or []
    
    @staticmethod
    def get_match_stats(user_id):
        """
        Get match statistics for a user.
        
        Args:
            user_id: User's ID
        
        Returns:
            Dict with win/loss/draw counts
        """
        query = """
            SELECT
                SUM(CASE WHEN winner_id = %s THEN 1 ELSE 0 END) as wins,
                SUM(CASE WHEN winner_id IS NULL AND (player1_id = %s OR player2_id = %s) THEN 1 ELSE 0 END) as draws,
                SUM(CASE WHEN winner_id IS NOT NULL AND winner_id != %s AND (player1_id = %s OR player2_id = %s) THEN 1 ELSE 0 END) as losses
            FROM match_history
            WHERE player1_id = %s OR player2_id = %s
        """
        result = DatabaseQuery.execute_query(
            query,
            (user_id, user_id, user_id, user_id, user_id, user_id, user_id, user_id),
            fetch_one=True
        )
        
        if result:
            return {
                'wins': result.get('wins') or 0,
                'draws': result.get('draws') or 0,
                'losses': result.get('losses') or 0
            }
        return {'wins': 0, 'draws': 0, 'losses': 0}

    @staticmethod
    def get_match_details(match_id):
        """
        Get match details including moves for replay.
        
        Args:
            match_id: Match ID
            
        Returns:
            Match dict or None
        """
        query = """
            SELECT m.id, m.game_type, m.mode, m.winner_id, m.played_at, m.moves,
                   p1.display_name as p1_name, p2.display_name as p2_name,
                   m.player1_id, m.player2_id
            FROM match_history m
            JOIN users p1 ON m.player1_id = p1.id
            JOIN users p2 ON m.player2_id = p2.id
            WHERE m.id = %s
        """
        return DatabaseQuery.execute_query(query, (match_id,), fetch_one=True)
