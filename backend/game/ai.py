"""
AI logic: Move generation using Minimax & Alpha-Beta Pruning.
Advanced AI with strategic thinking for both Tic-Tac-Toe and Caro.
"""
import random
import math
from game.engine import GameEngine


class AIPlayer:
    """Advanced AI logic for Tic-Tac-Toe and Caro games."""
    
    # Heuristic scores for Caro pattern evaluation
    SCORES = {
        'WIN': 10000000,           # 5 in a row
        'OPEN_4': 100000,          # 4 with both ends open
        'BLOCKED_4': 10000,        # 4 with one end blocked
        'OPEN_3': 5000,            # 3 with both ends open
        'BLOCKED_3': 100,          # 3 with one end blocked
        'OPEN_2': 50,              # 2 with both ends open
        'BLOCKED_2': 10            # 2 with one end blocked
    }
    
    # Cache for Tic-Tac-Toe minimax results (state serialization -> score)
    TTT_CACHE = {}

    @staticmethod
    def get_ai_move(board, game_type, difficulty):
        """
        Main entry point to get AI move.
        
        Args:
            board: Game board state
            game_type: 'tic-tac-toe' or 'caro'
            difficulty: 'easy', 'medium', or 'hard'
        
        Returns:
            Tuple (r, c) for the move
        """
        if game_type == 'tic-tac-toe':
            return AIPlayer._get_tictactoe_move(board, difficulty)
        elif game_type == 'caro':
            return AIPlayer._get_caro_move(board, difficulty)
        return None
    
    # ========== TIC-TAC-TOE LOGIC ==========
    
    @staticmethod
    def _get_tictactoe_move(board, difficulty):
        """
        Get AI move for Tic-Tac-Toe (3x3 board).
        
        Easy: Random moves
        Medium: 30% random, 70% Minimax (occasional mistakes)
        Hard: Full Minimax with Alpha-Beta Pruning (unbeatable)
        """
        empty = [(r, c) for r in range(3) for c in range(3) if board[r][c] == 0]
        if not empty:
            return None
        
        # EASY: Pure random
        if difficulty == 'easy':
            return random.choice(empty)
        
        # Always prioritize immediate wins/blocks before deeper search
        winning_move = AIPlayer._find_immediate_ttt_move(board, 2)
        if winning_move:
            return winning_move
        blocking_move = AIPlayer._find_immediate_ttt_move(board, 1)
        if blocking_move:
            return blocking_move

        # MEDIUM: Occasionally random, otherwise use heuristic priority before minimax
        if difficulty == 'medium':
            if random.random() < 0.2:
                return random.choice(empty)
            heuristic_move = AIPlayer._pick_ttt_priority_move(board)
            if heuristic_move:
                return heuristic_move

        # HARD: Full Minimax with Alpha-Beta Pruning
        best_score = -math.inf
        best_move = random.choice(empty)  # Fallback
        cache = AIPlayer.TTT_CACHE
        
        for r, c in empty:
            board[r][c] = 2  # AI is player 2
            score = AIPlayer._minimax_ttt(board, 0, False, -math.inf, math.inf, cache)
            board[r][c] = 0  # Undo
            
            if score > best_score:
                best_score = score
                best_move = (r, c)
        
        return best_move

    @staticmethod
    def _find_immediate_ttt_move(board, player):
        """Return a move that lets `player` win on this turn if available."""
        for r in range(3):
            for c in range(3):
                if board[r][c] != 0:
                    continue
                board[r][c] = player
                if AIPlayer._check_winner_simple(board) == player:
                    board[r][c] = 0
                    return (r, c)
                board[r][c] = 0
        return None

    @staticmethod
    def _pick_ttt_priority_move(board):
        """Prefer center, then corners, then edges for more human-like play."""
        priority = [
            (1, 1),  # center
            (0, 0), (0, 2), (2, 0), (2, 2),  # corners
            (0, 1), (1, 0), (1, 2), (2, 1)   # edges
        ]
        for r, c in priority:
            if board[r][c] == 0:
                return (r, c)
        return None

    @staticmethod
    def _serialize_ttt(board):
        """Convert Tic-Tac-Toe board to immutable representation for caching."""
        return tuple(cell for row in board for cell in row)

    @staticmethod
    def _minimax_ttt(board, depth, is_maximizing, alpha, beta, cache=None):
        """
        Minimax algorithm with Alpha-Beta Pruning for Tic-Tac-Toe.
        
        Args:
            board: Current board state
            depth: Current recursion depth
            is_maximizing: True if maximizing player (AI), False if minimizing (human)
            alpha: Alpha value for pruning
            beta: Beta value for pruning
        
        Returns:
            Score for the board state
        """  # noqa: D400
        state_key = None
        if cache is not None:
            state_key = (AIPlayer._serialize_ttt(board), depth, is_maximizing)
            cached_score = cache.get(state_key)
            if cached_score is not None:
                return cached_score
        
        # Check terminal state
        winner = AIPlayer._check_winner_simple(board)
        if winner == 2:
            return 10 - depth  # AI wins (prefer faster wins)
        if winner == 1:
            return depth - 10  # Human wins (prefer slower losses)
        if winner == 'draw':
            return 0

        if is_maximizing:
            # AI's turn (maximize score)
            max_eval = -math.inf
            for r in range(3):
                for c in range(3):
                    if board[r][c] == 0:
                        board[r][c] = 2
                        eval_score = AIPlayer._minimax_ttt(board, depth + 1, False, alpha, beta, cache)
                        board[r][c] = 0
                        max_eval = max(max_eval, eval_score)
                        alpha = max(alpha, eval_score)
                        if beta <= alpha:
                            break  # Beta cutoff
            result = max_eval
        else:
            # Human's turn (minimize score)
            min_eval = math.inf
            for r in range(3):
                for c in range(3):
                    if board[r][c] == 0:
                        board[r][c] = 1
                        eval_score = AIPlayer._minimax_ttt(board, depth + 1, True, alpha, beta, cache)
                        board[r][c] = 0
                        min_eval = min(min_eval, eval_score)
                        beta = min(beta, eval_score)
                        if beta <= alpha:
                            break  # Alpha cutoff
            result = min_eval
        
        if cache is not None and state_key is not None:
            cache[state_key] = result
        return result

    @staticmethod
    def _check_winner_simple(board):
        """
        Fast winner check for 3x3 board.
        
        Returns:
            1 (human wins), 2 (AI wins), 'draw', or None (game continues)
        """
        # Check rows and columns
        lines = board + [list(col) for col in zip(*board)]
        
        # Check diagonals
        lines.append([board[i][i] for i in range(3)])
        lines.append([board[i][2-i] for i in range(3)])
        
        # Check for winner
        for line in lines:
            if line[0] != 0 and all(x == line[0] for x in line):
                return line[0]
        
        # Check for draw
        if all(cell != 0 for row in board for cell in row):
            return 'draw'
        
        return None

    # ========== CARO LOGIC (ADVANCED) ==========
    
    @staticmethod
    def _get_caro_move(board, difficulty):
        """
        Get AI move for Caro/Gomoku (15x20 board).
        
        Easy: Random moves from neighbor positions
        Medium: Depth 1 Minimax (basic tactics)
        Hard: Depth 2 Minimax (strategic thinking)
        """
        # Get possible moves (only near existing pieces)
        search_radius = 3 if difficulty == 'hard' else 2
        possible_moves = AIPlayer._get_neighbor_moves(board, radius=search_radius)
        if not possible_moves:
            # Empty board: play in center
            return (len(board) // 2, len(board[0]) // 2)

        # EASY: Random move from neighbors
        if difficulty == 'easy':
            return random.choice(possible_moves)

        # Look for immediate wins or urgent defensive blocks before deeper search
        winning_move = AIPlayer._find_immediate_caro_move(board, possible_moves, 2)
        if winning_move:
            return winning_move
        blocking_move = AIPlayer._find_immediate_caro_move(board, possible_moves, 1)
        if blocking_move:
            return blocking_move

        # VCF (Victory by Continuous Fours): look for unstoppable 4-threats
        vcf_move = AIPlayer._find_vcf_move(board, possible_moves, 2)
        if vcf_move:
            return vcf_move

        ordered_moves = possible_moves
        if difficulty == 'hard':
            ordered_moves = AIPlayer._order_moves_by_urgency(board, possible_moves, 2, limit=20)

        # MEDIUM/HARD: Minimax with depth limit
        depth = 2 if difficulty == 'hard' else 1
        
        best_score = -math.inf
        best_move = ordered_moves[0]  # Default fallback
        
        # Evaluate each possible move
        for r, c in ordered_moves:
            board[r][c] = 2  # AI plays here
            
            # Immediate win check
            if AIPlayer._check_caro_win_local(board, r, c, 2):
                board[r][c] = 0
                return (r, c)  # Take winning move immediately
            
            # Minimax evaluation
            score = AIPlayer._minimax_caro(board, depth - 1, False, -math.inf, math.inf, (r, c))
            board[r][c] = 0  # Undo
            
            if score > best_score:
                best_score = score
                best_move = (r, c)
        
        return best_move

    @staticmethod
    def _find_immediate_caro_move(board, moves, player):
        """Return move that lets `player` win immediately, if any."""
        for r, c in moves:
            if board[r][c] != 0:
                continue
            board[r][c] = player
            if AIPlayer._check_caro_win_local(board, r, c, player):
                board[r][c] = 0
                return (r, c)
            board[r][c] = 0
        return None

    @staticmethod
    def _find_vcf_move(board, moves, player):
        """Find move that creates an open four (continuous threat)."""
        for r, c in moves:
            if board[r][c] != 0:
                continue
            board[r][c] = player
            if AIPlayer._creates_open_four(board, r, c, player):
                board[r][c] = 0
                return (r, c)
            board[r][c] = 0
        return None

    @staticmethod
    def _creates_open_four(board, r, c, player):
        """Check if placing at (r,c) creates an open four threat."""
        rows, cols = len(board), len(board[0])
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            open_ends = 0

            # forward
            nr, nc = r + dr, c + dc
            while 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == player:
                count += 1
                nr += dr
                nc += dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == 0:
                open_ends += 1

            # backward
            nr, nc = r - dr, c - dc
            while 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == player:
                count += 1
                nr -= dr
                nc -= dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == 0:
                open_ends += 1

            if count == 4 and open_ends == 2:
                return True
        return False

    @staticmethod
    def _order_moves_by_urgency(board, moves, player, limit=None):
        """Sort moves by local pattern potential and optionally trim."""
        scored = []
        for move in moves:
            score = AIPlayer._local_pattern_score(board, move[0], move[1], player)
            scored.append((score, move))
        scored.sort(key=lambda item: item[0], reverse=True)
        ordered = [move for _, move in scored]
        if limit:
            ordered = ordered[:limit]
        return ordered

    @staticmethod
    def _local_pattern_score(board, r, c, player):
        """Heuristic that rewards moves extending lines or creating forks."""
        if board[r][c] != 0:
            return 0
        board[r][c] = player
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        max_run = 0
        total = 0
        for dr, dc in directions:
            forward = AIPlayer._count_direction(board, r, c, dr, dc, player)
            backward = AIPlayer._count_direction(board, r, c, -dr, -dc, player)
            run = 1 + forward + backward
            max_run = max(max_run, run)
            total += run
        board[r][c] = 0
        # Weight longest run heavily but keep some awareness of additional lines
        return max_run * 100 + total

    @staticmethod
    def _count_direction(board, r, c, dr, dc, player):
        """Count consecutive stones for `player` starting from (r,c) exclusive."""
        rows, cols = len(board), len(board[0])
        count = 0
        nr, nc = r + dr, c + dc
        while 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == player:
            count += 1
            nr += dr
            nc += dc
        return count

    @staticmethod
    def _order_moves(board, moves, player):
        """Order moves by heuristic board score to improve alpha-beta pruning."""
        scored_moves = []
        for r, c in moves:
            board[r][c] = player
            score = AIPlayer._evaluate_board(board)
            board[r][c] = 0
            scored_moves.append((score, (r, c)))
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        return [move for _, move in scored_moves]

    @staticmethod
    def _minimax_caro(board, depth, is_maximizing, alpha, beta, last_move):
        """
        Minimax algorithm with Alpha-Beta Pruning for Caro.
        
        Args:
            board: Current board state
            depth: Remaining depth to search
            is_maximizing: True if AI's turn, False if human's turn
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            last_move: Last move position (r, c)
        
        Returns:
            Score for the board state
        """
        last_r, last_c = last_move
        player_check = 2 if not is_maximizing else 1  # Who just played
        
        # Check if last move resulted in a win
        if AIPlayer._check_caro_win_local(board, last_r, last_c, player_check):
            return 10000000 if player_check == 2 else -10000000
        
        # Depth limit reached: evaluate board
        if depth == 0:
            return AIPlayer._evaluate_board(board)

        # Get possible moves (narrower search at deeper levels)
        radius = 2 if depth > 1 else 1
        possible_moves = AIPlayer._get_neighbor_moves(board, radius=radius)
        
        if not possible_moves:
            return AIPlayer._evaluate_board(board)
        
        if len(possible_moves) > 18:
            focus_player = 2 if is_maximizing else 1
            possible_moves = AIPlayer._order_moves_by_urgency(board, possible_moves, focus_player, limit=18)

        possible_moves = AIPlayer._order_moves(board, possible_moves, 2 if is_maximizing else 1)
        
        if is_maximizing:
            # AI's turn (maximize)
            max_eval = -math.inf
            for r, c in possible_moves:
                board[r][c] = 2
                eval_score = AIPlayer._minimax_caro(board, depth - 1, False, alpha, beta, (r, c))
                board[r][c] = 0
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            # Human's turn (minimize)
            min_eval = math.inf
            for r, c in possible_moves:
                board[r][c] = 1
                eval_score = AIPlayer._minimax_caro(board, depth - 1, True, alpha, beta, (r, c))
                board[r][c] = 0
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval

    @staticmethod
    def _get_neighbor_moves(board, radius=1):
        """
        Get valid moves only around existing pieces (localized search).
        
        This optimization reduces search space from 300 cells to ~20-50 cells.
        
        Args:
            board: Game board
            radius: Search radius around pieces (1 or 2)
        
        Returns:
            List of (r, c) tuples for valid moves
        """
        rows, cols = len(board), len(board[0])
        moves = set()
        has_piece = False
        
        # Find all empty cells near existing pieces
        for r in range(rows):
            for c in range(cols):
                if board[r][c] != 0:
                    has_piece = True
                    # Check cells in radius around this piece
                    for i in range(-radius, radius + 1):
                        for j in range(-radius, radius + 1):
                            nr, nc = r + i, c + j
                            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == 0:
                                moves.add((nr, nc))
        
        if not has_piece:
            return []  # Empty board
        
        return sorted(moves)

    @staticmethod
    def _check_caro_win_local(board, r, c, player):
        """
        Fast win check only around the last move position.
        
        Args:
            board: Game board
            r, c: Position of last move
            player: Player number (1 or 2)
        
        Returns:
            True if player has 5 in a row, False otherwise
        """
        rows, cols = len(board), len(board[0])
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            count = 1
            
            # Check forward direction
            for k in range(1, 5):
                nr, nc = r + dr * k, c + dc * k
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == player:
                    count += 1
                else:
                    break
            
            # Check backward direction
            for k in range(1, 5):
                nr, nc = r - dr * k, c - dc * k
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == player:
                    count += 1
                else:
                    break
            
            # Check if we have 5 in a row
            if count >= 5:
                return True
        
        return False

    @staticmethod
    def _evaluate_board(board):
        """
        Heuristic board evaluation function.
        
        Evaluates the board state based on piece patterns.
        
        Returns:
            Score (positive favors AI, negative favors human)
        """
        ai_score = AIPlayer._evaluate_role(board, 2)
        human_score = AIPlayer._evaluate_role(board, 1)
        
        # AI score minus weighted human score (weight 1.2 for defensive bias)
        return ai_score - (human_score * 2.0)

    @staticmethod
    def _evaluate_role(board, player_val):
        """
        Calculate score for a player based on piece patterns.
        
        Args:
            board: Game board
            player_val: Player number (1 or 2)
        
        Returns:
            Total score for the player
        """
        score = 0
        rows, cols = len(board), len(board[0])
        
        # Evaluate horizontal lines
        for r in range(rows):
            score += AIPlayer._evaluate_line(board[r], player_val)
        
        # Evaluate vertical lines
        for c in range(cols):
            col_arr = [board[r][c] for r in range(rows)]
            score += AIPlayer._evaluate_line(col_arr, player_val)
        
        # Evaluate diagonal lines (top-left to bottom-right)
        for start_row in range(rows - 4):
            diag = []
            r, c = start_row, 0
            while r < rows and c < cols:
                diag.append(board[r][c])
                r += 1
                c += 1
            score += AIPlayer._evaluate_line(diag, player_val)
        for start_col in range(1, cols - 4):
            diag = []
            r, c = 0, start_col
            while r < rows and c < cols:
                diag.append(board[r][c])
                r += 1
                c += 1
            score += AIPlayer._evaluate_line(diag, player_val)
        
        # Evaluate anti-diagonal lines (top-right to bottom-left)
        for start_col in range(4, cols):
            diag = []
            r, c = 0, start_col
            while r < rows and c >= 0:
                diag.append(board[r][c])
                r += 1
                c -= 1
            score += AIPlayer._evaluate_line(diag, player_val)
        for start_row in range(1, rows - 4):
            diag = []
            r, c = start_row, cols - 1
            while r < rows and c >= 0:
                diag.append(board[r][c])
                r += 1
                c -= 1
            score += AIPlayer._evaluate_line(diag, player_val)
        
        return score

    @staticmethod
    def _evaluate_line(line, player_val):
        """Evaluate all 5-cell windows within a given line."""
        if len(line) < 5:
            return 0
        score = 0
        length = len(line)
        for start in range(length - 4):
            window = line[start:start+5]
            before = line[start - 1] if start > 0 else None
            after = line[start + 5] if (start + 5) < length else None
            score += AIPlayer._evaluate_window(window, before, after, player_val)
        return score

    @staticmethod
    def _evaluate_window(window, before, after, player_val):
        """
        Evaluate a 5-cell window and return score.
        
        Args:
            window: List of 5 cell values
            player_val: Player to evaluate (1 or 2)
        
        Returns:
            Score for this window
        """
        score = 0
        opp_val = 1 if player_val == 2 else 2
        
        player_count = window.count(player_val)
        opp_count = window.count(opp_val)
        
        # Mixed windows are neutral
        if player_count > 0 and opp_count > 0:
            return 0
        
        if player_count == 0:
            return 0
        
        # Determine how many ends are open (empty)
        open_ends = 0
        if before == 0:
            open_ends += 1
        if after == 0:
            open_ends += 1
        
        # Assign score based on pattern
        if player_count == 5:
            score += AIPlayer.SCORES['WIN']
        elif player_count == 4:
            if open_ends == 2:
                score += AIPlayer.SCORES['OPEN_4']
            elif open_ends == 1:
                score += AIPlayer.SCORES['BLOCKED_4']
        elif player_count == 3:
            if open_ends == 2:
                score += AIPlayer.SCORES['OPEN_3']
            elif open_ends == 1:
                score += AIPlayer.SCORES['BLOCKED_3']
        elif player_count == 2:
            if open_ends == 2:
                score += AIPlayer.SCORES['OPEN_2']
            elif open_ends == 1:
                score += AIPlayer.SCORES['BLOCKED_2']
        elif player_count == 1 and open_ends == 2:
            score += 5  # Encourage extending isolated stones
        
        return score
