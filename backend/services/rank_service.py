"""
Ranking service: User level calculation, rank updates, level history logging.
Database-driven implementation using game_levels and tiers tables.
"""
from database.db import DatabaseQuery, DatabaseConnection
from mysql.connector import Error


class RankService:
    """Handles ranking, leveling, and rank point management."""
    
    @staticmethod
    def get_level_from_score(rank_score):
        """
        Query database to find level corresponding to score.
        Logic: Find highest level where required_score <= current score.
        
        Args:
            rank_score: User's current rank score
            
        Returns:
            User level (1-500)
        """
        # Negative scores default to level 1
        if rank_score < 0:
            return 1
        
        query = """
            SELECT level 
            FROM game_levels 
            WHERE required_score <= %s 
            ORDER BY level DESC 
            LIMIT 1
        """
        result = DatabaseQuery.execute_query(query, (rank_score,), fetch_one=True)
        
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
    def log_level_change(user_id, level, rank_score):
        """
        Log a user's level change to history.
        
        Args:
            user_id: User's ID
            level: New level
            rank_score: New rank score
        
        Returns:
            True if logged, False otherwise
        """
        query = """
            INSERT INTO user_levels_history (user_id, level, rank_score)
            VALUES (%s, %s, %s)
        """
        try:
            DatabaseQuery.execute_update(query, (user_id, level, rank_score))
            return True
        except Exception as e:
            print(f"Failed to log level change: {e}")
            return False
    
    @staticmethod
    def update_rank(user_id, points):
        """
        Update user's rank score and recalculate level from database.
        
        Args:
            user_id: User's ID
            points: Points to add (positive or negative)
        
        Returns:
            True if successful, False otherwise
        """
        conn = DatabaseConnection.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor(dictionary=True)
            
            # 1. Get current score and level
            cursor.execute("SELECT rank_score, user_level FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if not user:
                return False
            
            current_score = user['rank_score']
            current_level = user['user_level']
            
            # 2. Calculate new score (minimum 0)
            new_score = max(0, current_score + points)
            
            # 3. Update score in database
            cursor.execute("UPDATE users SET rank_score = %s WHERE id = %s", (new_score, user_id))
            
            # 4. Query game_levels table to get new level
            cursor.execute(
                "SELECT level FROM game_levels WHERE required_score <= %s ORDER BY level DESC LIMIT 1", 
                (new_score,)
            )
            level_row = cursor.fetchone()
            new_level = level_row['level'] if level_row else 1
            
            # 5. If level changed -> Update level and log history
            if new_level != current_level:
                cursor.execute("UPDATE users SET user_level = %s WHERE id = %s", (new_level, user_id))
                
                # Log level-up
                cursor.execute(
                    "INSERT INTO user_levels_history (user_id, level, rank_score) VALUES (%s, %s, %s)",
                    (user_id, new_level, new_score)
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
            updates: List of tuples (user_id, points)
        
        Returns:
            True if all updates succeed, False otherwise
        """
        for user_id, points in updates:
            if not RankService.update_rank(user_id, points):
                return False
        return True
