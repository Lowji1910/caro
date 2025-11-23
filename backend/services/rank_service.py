"""
Ranking service: User level calculation, rank updates, level history logging.
Database-driven implementation using game_levels and tiers tables.
"""
from database.db import DatabaseQuery, DatabaseConnection
from mysql.connector import Error


class RankService:
    """Handles ranking, leveling, and rank point management."""
    
    @staticmethod
    def get_level_from_score(xp):
        """
        Query database to find level corresponding to XP.
        Logic: Find highest level where required_score <= current XP.
        
        Args:
            xp: User's current XP
            
        Returns:
            User level (1-500)
        """
        # Negative XP default to level 1
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
        
        # Return level if found, else default to 1
        return result['level'] if result else 1

    @staticmethod
    def get_tier_info(level):
        """
        Query database to get tier information based on level.
        
        Args:
            level: User's level
            
        Returns:
            Dict with tier name, color, and description
        """
        query = """
            SELECT name, color, description 
            FROM tiers 
            WHERE %s BETWEEN min_level AND max_level 
            LIMIT 1
        """
        result = DatabaseQuery.execute_query(query, (level,), fetch_one=True)
        
        # Fallback if tier not configured for this level
        if not result:
            return {'name': 'Tân Thủ', 'color': '#9E9E9E', 'description': 'Người mới'}
            
        return result
    
    @staticmethod
    def log_level_change(user_id, level, xp):
        """
        Log a user's level change to history.
        
        Args:
            user_id: User's ID
            level: New level
            xp: New XP
        
        Returns:
            True if logged, False otherwise
        """
        query = """
            INSERT INTO user_levels_history (user_id, level, xp)
            VALUES (%s, %s, %s)
        """
        try:
            DatabaseQuery.execute_update(query, (user_id, level, xp))
            return True
        except Exception as e:
            print(f"Failed to log level change: {e}")
            return False
    
    @staticmethod
    def update_rank(user_id, rank_points_delta, xp_delta):
        """
        Update user's XP and rank points.
        
        Args:
            user_id: User's ID
            rank_points_delta: Points to add/subtract from rank (can be negative)
            xp_delta: XP to add (always positive)
        
        Returns:
            True if successful, False otherwise
        """
        conn = DatabaseConnection.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor(dictionary=True)
            
            # 1. Get current values
            cursor.execute("SELECT xp, level, rank_points FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if not user:
                return False
            
            current_xp = user['xp']
            current_level = user['level']
            current_rank_points = user['rank_points']
            
            # 2. Calculate new values
            new_xp = current_xp + xp_delta
            new_rank_points = max(0, current_rank_points + rank_points_delta)
            
            # 3. Calculate new rank_id
            from services.user_service import UserService
            new_rank_id = UserService.calculate_rank_id(new_rank_points)
            
            # 4. Calculate new level from game_levels table
            cursor.execute(
                "SELECT level FROM game_levels WHERE required_score <= %s ORDER BY level DESC LIMIT 1", 
                (new_xp,)
            )
            level_row = cursor.fetchone()
            new_level = level_row['level'] if level_row else 1
            
            # 5. Update database
            cursor.execute(
                "UPDATE users SET xp = %s, level = %s, rank_points = %s, rank_id = %s WHERE id = %s",
                (new_xp, new_level, new_rank_points, new_rank_id, user_id)
            )
            
            # 6. If level changed -> Log history
            if new_level != current_level:
                cursor.execute(
                    "INSERT INTO user_levels_history (user_id, level, xp) VALUES (%s, %s, %s)",
                    (user_id, new_level, new_xp)
                )
                print(f"User {user_id} level changed: {current_level} -> {new_level}")

            conn.commit()
            cursor.close()
            return True
            
        except Exception as e:
            print(f"Error updating rank: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            DatabaseConnection.close_connection(conn)
    
    @staticmethod
    def update_rank_batch(updates):
        """
        Update ranks for multiple users in a transaction.
        
        Args:
            updates: List of tuples (user_id, rank_points_delta, xp_delta)
        
        Returns:
            True if all updates succeed, False otherwise
        """
        for user_id, rank_points_delta, xp_delta in updates:
            if not RankService.update_rank(user_id, rank_points_delta, xp_delta):
                return False
        return True
