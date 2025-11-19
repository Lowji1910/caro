import random
import copy

class GameEngine:
    def __init__(self):
        pass

    def create_board(self, game_type):
        if game_type == 'tic-tac-toe':
            return [[0 for _ in range(3)] for _ in range(3)]
        elif game_type == 'caro':
            return [[0 for _ in range(20)] for _ in range(15)]
        return []

    def check_winner(self, board, game_type, last_move):
        if not last_move:
            return 0, None
            
        r, c = last_move['r'], last_move['c']
        player = board[r][c]
        if player == 0: return 0, None

        rows = len(board)
        cols = len(board[0])
        win_len = 3 if game_type == 'tic-tac-toe' else 5
        
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dr, dc in directions:
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
            
            if len(line) >= win_len:
                return player, line

        is_full = True
        for row in board:
            if 0 in row:
                is_full = False
                break
        
        if is_full:
            return 'draw', None

        return 0, None

    # --- AI LOGIC ---

    def get_ai_move(self, board, game_type, difficulty):
        if game_type == 'tic-tac-toe':
            return self._get_tictactoe_move(board, difficulty)
        else:
            return self._get_caro_move(board, difficulty)

    def _get_tictactoe_move(self, board, difficulty):
        empty = [(r, c) for r in range(3) for c in range(3) if board[r][c] == 0]
        if not empty: return None

        # EASY: Random
        if difficulty == 'easy':
            return random.choice(empty)
            
        # HARD: Minimax (Unbeatable)
        # Player 2 is AI (Maximizing), Player 1 is Human (Minimizing)
        best_score = -float('inf')
        best_move = random.choice(empty) # Fallback

        for (r, c) in empty:
            board[r][c] = 2
            score = self._minimax(board, 0, False)
            board[r][c] = 0
            if score > best_score:
                best_score = score
                best_move = (r, c)
        
        return best_move

    def _minimax(self, board, depth, is_maximizing):
        # Simple static check
        # Note: This is simplified. In real implementation, need to pass last_move or scan board
        # Here we scan quickly for terminal state
        winner = self._scan_winner_full(board)
        if winner == 2: return 10 - depth
        if winner == 1: return depth - 10
        if winner == 'draw': return 0

        if is_maximizing:
            best_score = -float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] == 0:
                        board[r][c] = 2
                        score = self._minimax(board, depth + 1, False)
                        board[r][c] = 0
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] == 0:
                        board[r][c] = 1
                        score = self._minimax(board, depth + 1, True)
                        board[r][c] = 0
                        best_score = min(score, best_score)
            return best_score

    def _scan_winner_full(self, board):
        # Helper for minimax to check state without last_move optimization
        lines = []
        # Rows & Cols
        for i in range(3):
            lines.append(board[i])
            lines.append([board[r][i] for r in range(3)])
        # Diagonals
        lines.append([board[i][i] for i in range(3)])
        lines.append([board[i][2-i] for i in range(3)])

        for line in lines:
            if line[0] != 0 and all(x == line[0] for x in line):
                return line[0]
        
        if all(cell != 0 for row in board for cell in row):
            return 'draw'
        return 0

    def _get_caro_move(self, board, difficulty):
        rows = len(board)
        cols = len(board[0])
        empty = [(r, c) for r in range(rows) for c in range(cols) if board[r][c] == 0]
        
        if not empty: return None

        # EASY: Random near center if possible
        if difficulty == 'easy':
            return random.choice(empty)

        # MEDIUM/HARD: Greedy Heuristic (Attack & Block)
        
        # 1. Check if AI can win immediately (4 in a row -> make 5)
        win_move = self._find_caro_threat(board, 2, 4) # Find 4 of AI
        if win_move: return win_move

        # 2. Block opponent winning (4 in a row)
        block_win = self._find_caro_threat(board, 1, 4) # Find 4 of Human
        if block_win: return block_win

        # 3. Create threats (3 in a row)
        grow_move = self._find_caro_threat(board, 2, 3)
        if grow_move: return grow_move

        # 4. Block opponent threats (3 in a row)
        block_grow = self._find_caro_threat(board, 1, 3)
        if block_grow: return block_grow

        # Fallback: Random near center
        center_r, center_c = rows // 2, cols // 2
        empty.sort(key=lambda p: abs(p[0]-center_r) + abs(p[1]-center_c))
        # Pick one of the top 5 closest to center
        return random.choice(empty[:5])

    def _find_caro_threat(self, board, player, count):
        rows = len(board)
        cols = len(board[0])
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 0:
                    # Hypothesize playing here
                    board[r][c] = player
                    
                    # Check if this creates 'count' length line
                    created_threat = False
                    for dr, dc in directions:
                        length = 1
                        # Check +
                        for k in range(1, 5):
                            nr, nc = r + dr*k, c + dc*k
                            if 0<=nr<rows and 0<=nc<cols and board[nr][nc] == player: length += 1
                            else: break
                        # Check -
                        for k in range(1, 5):
                            nr, nc = r - dr*k, c - dc*k
                            if 0<=nr<rows and 0<=nc<cols and board[nr][nc] == player: length += 1
                            else: break
                        
                        if length >= count:
                            created_threat = True
                            break
                    
                    board[r][c] = 0 # Undo
                    if created_threat:
                        return (r, c)
        return None