"""
Database connection and query utilities.
Handles all MySQL operations with proper error handling.
"""
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


class DatabaseConnection:
    """Manages MySQL database connections."""
    
    @staticmethod
    def get_connection():
        """
        Create and return a MySQL connection.
        Returns None if connection fails.
        """
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except Error as e:
            print(f"Database connection error: {e}")
            return None
    
    @staticmethod
    def close_connection(conn):
        """Safely close a database connection."""
        if conn and conn.is_connected():
            conn.close()


class DatabaseQuery:
    """Utility class for common database operations."""
    
    @staticmethod
    def execute_query(query, params=None, fetch_one=False, fetch_all=False):
        """
        Execute a SELECT query and return results.
        
        Args:
            query: SQL query string
            params: Tuple of parameters for the query
            fetch_one: If True, return single row as dict
            fetch_all: If True, return all rows as list of dicts
        
        Returns:
            Single dict, list of dicts, or None based on fetch flags
        """
        conn = DatabaseConnection.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            else:
                result = None
            
            cursor.close()
            return result
        except Error as e:
            print(f"Query execution error: {e}")
            return None
        finally:
            DatabaseConnection.close_connection(conn)
    
    @staticmethod
    def execute_update(query, params=None):
        """
        Execute an INSERT, UPDATE, or DELETE query.
        
        Args:
            query: SQL query string
            params: Tuple of parameters for the query
        
        Returns:
            lastrowid for INSERT, affected rows count, or None on error
        """
        conn = DatabaseConnection.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            
            result = cursor.lastrowid if cursor.lastrowid else cursor.rowcount
            cursor.close()
            return result
        except Error as e:
            print(f"Update execution error: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            DatabaseConnection.close_connection(conn)
    
    @staticmethod
    def execute_transaction(operations):
        """
        Execute multiple operations in a single transaction.
        
        Args:
            operations: List of tuples (query, params)
        
        Returns:
            True if all operations succeed, False otherwise
        """
        conn = DatabaseConnection.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            for query, params in operations:
                cursor.execute(query, params or ())
            conn.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Transaction error: {e}")
            conn.rollback()
            return False
        finally:
            DatabaseConnection.close_connection(conn)
