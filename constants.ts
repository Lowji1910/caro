// Colors derived from prompt
export const COLORS = {
  primaryBlue: '#6B8EFF',
  primaryPink: '#FF6B9D',
  primaryYellow: '#FFD93D',
  primaryGreen: '#6BCF7F',
  textPrimary: '#2D3748',
  textSecondary: '#718096',
  gridColor: '#E0E0E0',
};

export const GRADIENTS = {
  bg1: 'from-[#667eea] to-[#764ba2]',
  bg2: 'from-[#f093fb] to-[#f5576c]',
  bg3: 'from-[#4facfe] to-[#00f2fe]',
};

export const GAME_CONFIG = {
  ticTacToe: {
    rows: 3,
    cols: 3,
    winCondition: 3,
  },
  caro: {
    rows: 15, // Reduced slightly from 30x15 for better mobile/tablet rendering, logically identical
    cols: 20,
    winCondition: 5,
  },
};

export const RANKS = {
  Bronze: { color: '#CD7F32', min: 0 },
  Silver: { color: '#C0C0C0', min: 500 },
  Gold: { color: '#FFD700', min: 1000 },
  Crystal: { color: '#E6E6FA', min: 2000 },
};