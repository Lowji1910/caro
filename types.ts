

export type PlayerId = 1 | 2;
export type CellValue = 0 | PlayerId;
export type GameType = 'tic-tac-toe' | 'caro';
export type GameMode = 'ranked' | 'practice' | 'local';
export type AIDifficulty = 'easy' | 'medium' | 'hard';
export type ViewState = 'AUTH' | 'SIGNUP' | 'DASHBOARD' | 'MATCHMAKING' | 'GAME' | 'PROFILE' | 'PRACTICE_DIFFICULTY' | 'REPLAY' | 'PUBLIC_PROFILE';

export interface UserProfile {
  id: number;
  username: string;
  display_name: string;
  full_name?: string;
  date_of_birth?: string;
  bio?: string;
  avatar_url?: string;
  rank_level: 'Bronze' | 'Silver' | 'Gold' | 'Crystal';
  rank_score: number;
  user_level?: number; // Level từ 1-500
}

export interface MatchHistory {
  id: number;
  player1_id: number;
  player2_id: number;
  winner_id: number | null;
  game_type: GameType;
  mode: GameMode;
  played_at: string;
  opponent_name: string;
  result: 'win' | 'loss' | 'draw';
}

export interface GameState {
  board: CellValue[][];
  currentPlayer: PlayerId;
  winner: PlayerId | 0 | 'draw';
  winningLine: { r: number; c: number }[] | null;
  history: { r: number; c: number; player: PlayerId }[];
  lastMove: { r: number; c: number } | null;
}

export interface MatchConfig {
  id: string;
  type: GameType;
  mode: GameMode;
  difficulty?: AIDifficulty;
  opponent: UserProfile | null;
}
