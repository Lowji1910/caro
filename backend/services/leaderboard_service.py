"""
Leaderboard service: Ranking queries and leaderboard generation.
"""
from database.db import DatabaseQuery


class LeaderboardService:
    """Handles leaderboard queries and ranking information."""
    
    @staticmethod
    def get_leaderboard(limit=10):
        """
        Get top players by rank score with tier information.
        
        Args:
            limit: Number of top players to return
        
        Returns:
            List of user records sorted by rank score with tier info
        """
        query = """
            SELECT 
                u.id, 
                u.display_name, 
                u.rank_score, 
                u.user_level,
                t.name as tier_name,
                t.color as tier_color
            FROM users u
            LEFT JOIN tiers t ON u.user_level BETWEEN t.min_level AND t.max_level
            ORDER BY u.rank_score DESC
            LIMIT %s
        """
        return DatabaseQuery.execute_query(query, (limit,), fetch_all=True) or []
    
    @staticmethod
    def get_user_rank(user_id):
        """
        Get a user's rank position on the leaderboard.
        
        Args:
            user_id: User's ID
        
        Returns:
            Rank position (1-based) or None if user not found
        """
        query = """
            SELECT COUNT(*) + 1 as rank
            FROM users
            WHERE rank_score > (SELECT rank_score FROM users WHERE id = %s)
        """
        result = DatabaseQuery.execute_query(query, (user_id,), fetch_one=True)
        return result['rank'] if result else None
    
    @staticmethod
    def get_leaderboard_by_game_type(game_type, limit=10):
        """
        Get leaderboard filtered by game type (if tracked separately).
        
        Args:
            game_type: 'tic-tac-toe' or 'caro'
            limit: Number of top players to return
        
        Returns:
            List of user records
        """
        # Note: Current schema doesn't separate scores by game type
        # This is a placeholder for future enhancement
        return LeaderboardService.get_leaderboard(limit)
    
    @staticmethod
    def get_nearby_players(user_id, range_size=5):
        """
        Get players ranked near the given user.
        
        Args:
            user_id: User's ID
            range_size: Number of players above and below to return
        
        Returns:
            List of nearby user records
        """
        user_rank = LeaderboardService.get_user_rank(user_id)
        if not user_rank:
            return []
        
        offset = max(0, user_rank - range_size - 1)
        query = """
            SELECT 
                u.id, u.display_name, u.rank_score, u.user_level,
                t.name as tier_name, t.color as tier_color
            FROM users u
            LEFT JOIN tiers t ON u.user_level BETWEEN t.min_level AND t.max_level
            ORDER BY u.rank_score DESC
            LIMIT %s OFFSET %s
        """
        return DatabaseQuery.execute_query(
            query,
            (range_size * 2 + 1, offset),
            fetch_all=True
        ) or []
