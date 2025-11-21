"""
User service: Authentication, profile management, password changes.
"""
from database.db import DatabaseQuery
from werkzeug.security import generate_password_hash, check_password_hash


class UserService:
    """Handles user authentication and profile operations."""
    
    @staticmethod
    def authenticate(username, password):
        """
        Authenticate user with username and password (HASHED).
        """
        # 1. Lấy thông tin user dựa trên username (KHÔNG so sánh password trong SQL nữa)
        query = "SELECT * FROM users WHERE username = %s"
        user = DatabaseQuery.execute_query(query, (username,), fetch_one=True)
        
        # 2. Nếu user tồn tại, dùng hàm check_password_hash để so sánh mật khẩu nhập vào với mật khẩu mã hóa trong DB
        if user and check_password_hash(user['password'], password):
            return user
            
        return None
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Fetch user by ID.
        
        Args:
            user_id: User's ID
        
        Returns:
            User dict or None
        """
        query = "SELECT * FROM users WHERE id = %s"
        return DatabaseQuery.execute_query(query, (user_id,), fetch_one=True)
    
    @staticmethod
    def get_user_by_username(username):
        """
        Fetch user by username.
        
        Args:
            username: User's username
        
        Returns:
            User dict or None
        """
        query = "SELECT id FROM users WHERE username = %s"
        return DatabaseQuery.execute_query(query, (username,), fetch_one=True)
    
    @staticmethod
    def create_user(username, password, display_name, email):
        """
        Create a new user account with HASHED password.
        """
        # Check if username exists
        if UserService.get_user_by_username(username):
            return None
            
        # Check if email exists
        email_check_query = "SELECT id FROM users WHERE email = %s"
        if DatabaseQuery.execute_query(email_check_query, (email,), fetch_one=True):
            return None # Email đã tồn tại
        
        # 1. Mã hóa mật khẩu
        hashed_password = generate_password_hash(password)

        # 2. Insert user với mật khẩu đã mã hóa và email
        query = """
            INSERT INTO users (username, password, display_name, full_name, email, rank_score, rank_level, user_level)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        # Truyền hashed_password và email vào query
        user_id = DatabaseQuery.execute_update(query, (
            username, 
            hashed_password, 
            display_name, 
            display_name, 
            email,
            0, 'Bronze', 1
        ))
        
        if user_id:
            return {
                'id': user_id,
                'username': username,
                'display_name': display_name,
                'email': email,
                'rank_score': 0,
                'rank_level': 'Bronze',
                'user_level': 1
            }
        return None
    
    @staticmethod
    def update_profile(user_id, **kwargs):
        """
        Update user profile fields.
        
        Args:
            user_id: User's ID
            **kwargs: Fields to update (full_name, display_name, date_of_birth, bio, etc.)
        
        Returns:
            Updated user dict or None
        """
        if not kwargs:
            return UserService.get_user_by_id(user_id)
        
        # Build dynamic UPDATE query
        update_fields = []
        update_values = []
        
        allowed_fields = ['full_name', 'display_name', 'date_of_birth', 'bio', 'avatar_url']
        for field in allowed_fields:
            if field in kwargs:
                update_fields.append(f"{field} = %s")
                update_values.append(kwargs[field])
        
        if not update_fields:
            return UserService.get_user_by_id(user_id)
        
        update_values.append(user_id)
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"
        DatabaseQuery.execute_update(query, tuple(update_values))
        
        return UserService.get_user_by_id(user_id)
    
    @staticmethod
    def change_password(user_id, old_password, new_password):
        """
        Change user's password.
        
        Args:
            user_id: User's ID
            old_password: Current password (for verification)
            new_password: New password
        
        Returns:
            True if successful, False otherwise
        """
        user = UserService.get_user_by_id(user_id)
        if not user or user['password'] != old_password:
            return False
        
        query = "UPDATE users SET password = %s WHERE id = %s"
        return DatabaseQuery.execute_update(query, (new_password, user_id)) is not None

    @staticmethod
    def get_public_profile(user_id):
        """
        Get public user profile (no sensitive data) with tier information.
        
        Args:
            user_id: User's ID
            
        Returns:
            User dict with tier info or None
        """
        query = """
            SELECT 
                u.id, u.display_name, u.full_name, u.bio, u.avatar_url, 
                u.rank_score, u.user_level, u.created_at,
                t.name as tier_name,
                t.color as tier_color,
                t.description as tier_description
            FROM users u
            LEFT JOIN tiers t ON u.user_level BETWEEN t.min_level AND t.max_level
            WHERE u.id = %s
        """
        return DatabaseQuery.execute_query(query, (user_id,), fetch_one=True)
