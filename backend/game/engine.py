"""
Game engine: Board creation, winner checking, game state management.
"""
from config import GAME_CONFIG, DIRECTIONS


class GameEngine:
    """Core game logic for Tic-Tac-Toe and Caro."""
    
    @staticmethod
    def create_board(game_type):
        """
        Create an empty game board.
        
        Args:
            game_type: 'tic-tac-toe' or 'caro'
        
        Returns:
            2D list representing the game board
        """
        config = GAME_CONFIG.get(game_type)
        if not config:
            return []
        
        rows = config['rows']
        cols = config['cols']
        return [[0 for _ in range(cols)] for _ in range(rows)]
    
    @staticmethod
    def check_winner(board, game_type, last_move):
        """
        Check if there's a winner after the last move.
        
        Args:
            board: Current game board
            game_type: 'tic-tac-toe' or 'caro'
            last_move: Dict with 'r' and 'c' keys for last move position
        
        Returns:
            Tuple (winner, winning_line) where:
            - winner: 1 (player 1), 2 (player 2), 'draw', or 0 (no winner)
            - winning_line: List of (r, c) tuples for winning positions, or None
        """
        if not last_move:
            return 0, None
        
        r, c = last_move['r'], last_move['c']
        player = board[r][c]
        
        if player == 0:
            return 0, None
        
        rows = len(board)
        cols = len(board[0])
        win_len = GAME_CONFIG[game_type]['win_length']
        
        # Check all four directions
        for dr, dc in DIRECTIONS:
            line = [(r, c)]
            
            # Check forward
            for i in range(1, win_len):
                nr, nc = r + dr * i, c + dc * i
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == player:
                    line.append((nr, nc))
                else:
                    break
            
            # Check backward
            for i in range(1, win_len):
                nr, nc = r - dr * i, c - dc * i
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == player:
                    line.append((nr, nc))
                else:
                    break
            
            # Check if we have a winning line
            if len(line) >= win_len:
                return player, line
        
        # Check for draw (board full)
        is_full = all(board[row][col] != 0 for row in range(rows) for col in range(cols))
        if is_full:
            return 'draw', None
        
        return 0, None
    
    @staticmethod
    def is_valid_move(board, r, c):
        """
        Check if a move is valid.
        
        Args:
            board: Current game board
            r: Row index
            c: Column index
        
        Returns:
            True if move is valid, False otherwise
        """
        rows = len(board)
        cols = len(board[0])
        
        if not (0 <= r < rows and 0 <= c < cols):
            return False
        
        return board[r][c] == 0
    
    @staticmethod
    def apply_move(board, r, c, player):
        """
        Apply a move to the board.
        
        Args:
            board: Current game board
            r: Row index
            c: Column index
            player: Player number (1 or 2)
        
        Returns:
            True if move was applied, False if invalid
        """
        if not GameEngine.is_valid_move(board, r, c):
            return False
        
        board[r][c] = player
        return True

    @staticmethod
    def undo_move(board, r, c):
        """
        Undo a move by clearing the cell.
        
        Args:
            board: Current game board
            r: Row index
            c: Column index
            
        Returns:
            True if successful, False if invalid coordinates
        """
        rows = len(board)
        cols = len(board[0])
        
        if 0 <= r < rows and 0 <= c < cols:
            board[r][c] = 0
            return True
        return False
