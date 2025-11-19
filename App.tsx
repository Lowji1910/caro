
import React, { useState, useEffect, useRef } from 'react';
import { 
  User as UserIcon, Lock, Trophy, 
  ChevronLeft, Sword, Clock, Info
} from 'lucide-react';
import { io, Socket } from 'socket.io-client';
import { 
  UserProfile, ViewState, MatchConfig, 
  GameState, GameMode, AIDifficulty, GameType
} from './types';
import { COLORS, GRADIENTS } from './constants';
import { getTierInfo } from './utils/tierUtils';
import Button from './components/Button';
import Header from './components/Header';
import GameBoard from './components/GameBoard';
import Signup from './components/Signup';
import Profile from './components/Profile';
import RankInfoModal from './components/RankInfoModal';
import PracticeDifficultySelector from './components/PracticeDifficultySelector';

const SOCKET_URL = 'http://localhost:5000';

export default function App() {
  // --- STATE ---
  const [view, setView] = useState<ViewState>('AUTH');
  const [user, setUser] = useState<UserProfile | null>(null);
  const [practiceGameType, setPracticeGameType] = useState<GameType>('tic-tac-toe');
  
  // Socket
  const socketRef = useRef<Socket | null>(null);
  
  // Match & Game State
  const [match, setMatch] = useState<MatchConfig | null>(null);
  const [gameState, setGameState] = useState<GameState>({
    board: [],
    currentPlayer: 1,
    winner: 0,
    winningLine: null,
    history: [],
    lastMove: null
  });
  const [playerNumber, setPlayerNumber] = useState<1 | 2 | null>(null);
  const [timeLeft, setTimeLeft] = useState(30);
  const timerIntervalRef = useRef<NodeJS.Timeout | null>(null);
  
  // UI State
  const [isLoading, setIsLoading] = useState(false);
  const [loginForm, setLoginForm] = useState({ username: '', password: '' });
  const [leaderboard, setLeaderboard] = useState<UserProfile[]>([]);
  const [showRankInfo, setShowRankInfo] = useState<'tic-tac-toe' | 'caro' | null>(null);


  // --- INIT EFFECT (Check localStorage) ---
  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      try {
        const parsed = JSON.parse(savedUser);
        setUser(parsed);
        setView('DASHBOARD');
      } catch (err) {
        localStorage.removeItem('user');
      }
    }
  }, []);

  // --- CONNECTION EFFECT ---
  useEffect(() => {
    const socket = io(SOCKET_URL);
    socketRef.current = socket;

    socket.on('connect', () => console.log('Connected to backend'));

    socket.on('match_found', (data: any) => {
      const gameType = data.gameType || 'tic-tac-toe';
      const playerNum = data.playerNumber || 1;
      
      setPlayerNumber(playerNum);
      setMatch({
        id: data.roomId,
        type: gameType,
        mode: data.mode || 'ranked',
        opponent: data.opponent,
        difficulty: data.difficulty
      });
      
      // Use board from backend directly
      const initialBoard = data.board || [];
      setGameState({
        board: initialBoard,
        currentPlayer: data.firstTurn || 1,
        winner: 0,
        winningLine: null,
        history: [],
        lastMove: null
      });
      setTimeLeft(30);
      setView('GAME');
    });

    socket.on('game_update', (data: any) => {
      setGameState(prev => ({
        ...prev,
        board: data.board,
        currentPlayer: data.currentPlayer,
        winner: data.winner,
        winningLine: data.winningLine,
        lastMove: data.lastMove
      }));
      setTimeLeft(30); // Reset timer on each move
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  // --- TIMER EFFECT ---
  useEffect(() => {
    if (view !== 'GAME' || gameState.winner !== 0) {
      if (timerIntervalRef.current) clearInterval(timerIntervalRef.current);
      return;
    }

    timerIntervalRef.current = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          return 30;
        }
        return prev - 1;
      });
    }, 1000);

    return () => {
      if (timerIntervalRef.current) clearInterval(timerIntervalRef.current);
    };
  }, [view, gameState.winner]);

  // --- API CALLS ---

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      const res = await fetch(`${SOCKET_URL}/api/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(loginForm)
      });
      
      if (!res.ok) throw new Error('Login failed');
      
      const data = await res.json();
      setUser(data);
      localStorage.setItem('user', JSON.stringify(data));
      setView('DASHBOARD');
    } catch (err) {
      alert('Invalid username or password');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSignup = async (username: string, password: string, display_name: string) => {
    setIsLoading(true);
    try {
      const res = await fetch(`${SOCKET_URL}/api/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password, display_name })
      });

      if (!res.ok) {
        const error = await res.json();
        throw new Error(error.error || 'Signup failed');
      }

      const data = await res.json();
      setUser(data);
      localStorage.setItem('user', JSON.stringify(data));
      setView('DASHBOARD');
    } catch (err) {
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    setUser(null);
    setView('AUTH');
    localStorage.removeItem('user');
  };

  const handleUpdateProfile = async (updated: Partial<UserProfile>) => {
    const newUser = { ...user, ...updated } as UserProfile;
    setUser(newUser);
    localStorage.setItem('user', JSON.stringify(newUser));
  };

  const fetchLeaderboard = async () => {
      try {
          const res = await fetch(`${SOCKET_URL}/api/leaderboard`);
          const data = await res.json();
          setLeaderboard(data);
      } catch (e) { console.error(e); }
  };

  const startMatchmaking = (type: GameType, mode: GameMode, difficulty?: AIDifficulty) => {
    if (!socketRef.current) return;
    
    setView('MATCHMAKING');
    setMatch({
        id: '',
        type,
        mode,
        difficulty,
        opponent: null
    });

    socketRef.current.emit('join_matchmaking', {
        userId: user?.id,
        type,
        mode,
        difficulty
    });
  };

  const handleMove = (r: number, c: number) => {
    if (!socketRef.current || !match?.id) return;
    socketRef.current.emit('make_move', {
        roomId: match.id,
        r, c,
        player: gameState.currentPlayer // 1
    });
  };

  const returnToDashboard = () => {
    setMatch(null);
    setView('DASHBOARD');
    fetchLeaderboard(); 
  };

  const handlePracticeMode = (type: GameType) => {
    setPracticeGameType(type);
    setView('PRACTICE_DIFFICULTY');
  };

  const handlePracticeDifficultySelect = (difficulty: AIDifficulty) => {
    startMatchmaking(practiceGameType, 'practice', difficulty);
  };

  // --- RENDER ---

  if (view === 'PRACTICE_DIFFICULTY') {
    return (
      <PracticeDifficultySelector
        gameType={practiceGameType}
        onSelect={handlePracticeDifficultySelect}
        onBack={() => setView('DASHBOARD')}
      />
    );
  }

  if (view === 'AUTH') {
    return (
      <div className={`min-h-screen w-full flex items-center justify-center bg-gradient-to-br ${GRADIENTS.bg1}`}>
        <div className="bg-white p-8 rounded-3xl shadow-lg w-full max-w-md border border-gray-200">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-600 mb-2">
              Ranked Arena
            </h1>
            <p className="text-gray-500 font-medium">MySQL + Flask + Socket.IO</p>
          </div>

          <form onSubmit={handleLogin} className="space-y-6">
            <div className="space-y-4">
              <div className="relative">
                <UserIcon className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 h-5 w-5" />
                <input 
                  type="text" 
                  placeholder="Username" 
                  value={loginForm.username}
                  onChange={e => setLoginForm({...loginForm, username: e.target.value})}
                  className="w-full pl-12 pr-4 py-4 bg-gray-50 border-2 border-transparent focus:border-blue-400 focus:bg-white rounded-xl outline-none transition-all font-medium text-gray-700"
                />
              </div>
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 h-5 w-5" />
                <input 
                  type="password" 
                  placeholder="Password" 
                  value={loginForm.password}
                  onChange={e => setLoginForm({...loginForm, password: e.target.value})}
                  className="w-full pl-12 pr-4 py-4 bg-gray-50 border-2 border-transparent focus:border-blue-400 focus:bg-white rounded-xl outline-none transition-all font-medium text-gray-700"
                />
              </div>
            </div>
            <Button type="submit" className="w-full py-4 text-lg shadow-blue-300/50 shadow-lg" loading={isLoading}>
              Login
            </Button>
            <Button 
              type="button"
              variant="secondary"
              className="w-full py-4 text-lg"
              onClick={() => setView('SIGNUP')}
            >
              Create Account
            </Button>
          </form>
        </div>
      </div>
    );
  }

  if (view === 'SIGNUP') {
    return (
      <Signup
        onSignup={handleSignup}
        onBackToLogin={() => setView('AUTH')}
      />
    );
  }

  if (view === 'MATCHMAKING') {
    return (
      <div className={`min-h-screen flex flex-col items-center justify-center bg-gradient-to-br ${GRADIENTS.bg3} text-white`}>
        <div className="relative mb-8">
           <div className="absolute inset-0 animate-ping rounded-full bg-white/30"></div>
           <div className="relative bg-white/20 backdrop-blur-md p-8 rounded-full border border-white/30 shadow-2xl">
              <Sword size={64} className="animate-pulse" />
           </div>
        </div>
        <h2 className="text-3xl font-bold mb-2">Connecting to Server...</h2>
        <Button variant="secondary" onClick={returnToDashboard}>Cancel</Button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 font-sans text-gray-800 relative overflow-hidden">
      {/* Background Blobs */}
      <div className="fixed -top-20 -left-20 w-96 h-96 bg-blue-200/30 rounded-full blur-3xl pointer-events-none mix-blend-multiply"></div>
      <div className="fixed top-1/3 -right-20 w-96 h-96 bg-pink-200/30 rounded-full blur-3xl pointer-events-none mix-blend-multiply"></div>
      
      {user && <Header user={user} onLogout={handleLogout} onProfile={() => setView('PROFILE')} />}

      <main className="container mx-auto p-4 lg:p-8 relative z-10">
        {view === 'DASHBOARD' && (
          <div className="max-w-5xl mx-auto space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Tic Tac Toe Card */}
              <div className="bg-white rounded-3xl p-8 shadow-lg shadow-blue-200 hover:shadow-2xl transition-all border border-gray-200 relative overflow-hidden">
                   <div className="w-14 h-14 bg-blue-100 text-blue-600 rounded-2xl flex items-center justify-center mb-6">
                     <span className="text-3xl font-bold">#</span>
                   </div>
                   <h2 className="text-3xl font-black text-gray-800 mb-2">Tic-Tac-Toe</h2>
                   <p className="text-gray-600 text-sm mb-4">Game chiến thuật 3x3 kinh điển</p>
                   <div className="flex flex-col gap-3 mt-8">
                     <Button onClick={() => startMatchmaking('tic-tac-toe', 'ranked')}>Trận Đấu Xếp Hạng</Button>
                     <Button variant="ghost" onClick={() => handlePracticeMode('tic-tac-toe')}>Luyện Tập (Chọn độ khó)</Button>
                     <Button 
                       variant="secondary" 
                       size="sm" 
                       onClick={() => setShowRankInfo('tic-tac-toe')}
                       className="!text-xs"
                     >
                       <Info size={14} className="mr-1" /> Xem Thông Tin Xếp Hạng
                     </Button>
                   </div>
              </div>

              {/* Caro Card */}
              <div className="bg-white rounded-3xl p-8 shadow-lg shadow-pink-200 hover:shadow-2xl transition-all border border-gray-200 relative overflow-hidden">
                   <div className="w-14 h-14 bg-pink-100 text-pink-600 rounded-2xl flex items-center justify-center mb-6">
                     <span className="text-3xl font-bold">●</span>
                   </div>
                   <h2 className="text-3xl font-black text-gray-800 mb-2">Caro (Gomoku)</h2>
                   <p className="text-gray-600 text-sm mb-4">Game xếp 5 liên tiếp trên bàn 15x20</p>
                   <div className="flex flex-col gap-3 mt-8">
                     <Button className="!bg-gradient-to-r !from-pink-400 !to-red-400" onClick={() => startMatchmaking('caro', 'ranked')}>Trận Đấu Xếp Hạng</Button>
                     <Button variant="ghost" onClick={() => handlePracticeMode('caro')}>Luyện Tập (Chọn độ khó)</Button>
                     <Button 
                       variant="secondary" 
                       size="sm" 
                       onClick={() => setShowRankInfo('caro')}
                       className="!text-xs"
                     >
                       <Info size={14} className="mr-1" /> Xem Thông Tin Xếp Hạng
                     </Button>
                   </div>
              </div>
            </div>

            {/* Leaderboard */}
            <div className="bg-white rounded-3xl p-6 border border-gray-200 shadow-lg">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-xl font-bold flex items-center gap-2">
                  <Trophy className="text-yellow-500" /> Live Leaderboard
                </h3>
                <Button size="sm" variant="ghost" onClick={fetchLeaderboard}>Refresh</Button>
              </div>
              <div className="space-y-3">
                 {leaderboard.length === 0 && <div className="text-center text-gray-400">Loading from MySQL...</div>}
                 {leaderboard.map((p, i) => {
                   const tierInfo = p.user_level ? getTierInfo(p.user_level) : null;
                   return (
                   <div key={i} className="flex items-center justify-between p-4 rounded-xl hover:bg-gray-50 transition-colors border border-gray-100">
                      <div className="flex items-center gap-3">
                        <span className="font-black text-lg text-gray-400 w-8">#{i+1}</span>
                        <div>
                          <div className="flex items-center gap-2">
                            <span className="font-bold text-gray-800">{p.display_name}</span>
                            {tierInfo && (
                              <span 
                                className="px-2 py-0.5 rounded-full text-white text-xs font-bold uppercase tracking-wider"
                                style={{ backgroundColor: tierInfo.color }}
                              >
                                {tierInfo.name}
                              </span>
                            )}
                          </div>
                          <div className="flex items-center gap-2 text-xs mt-1">
                            <span className="bg-blue-100 text-blue-700 px-2 py-0.5 rounded font-bold">{p.rank_level}</span>
                            {p.user_level && (
                              <span className="text-gray-600">Lv {p.user_level}</span>
                            )}
                          </div>
                        </div>
                      </div>
                      <div className="font-bold text-blue-600 text-lg">{p.rank_score} pts</div>
                   </div>
                   );
                 })}
              </div>
            </div>
          </div>
        )}

        {view === 'PROFILE' && user && (
          <Profile
            user={user}
            onBack={() => setView('DASHBOARD')}
            onUpdate={handleUpdateProfile}
            onLogout={handleLogout}
            socketURL={SOCKET_URL}
          />
        )}

        {view === 'GAME' && match && (
          <div className="flex flex-col lg:flex-row h-[calc(100vh-100px)] gap-4">
             <div className="w-full lg:w-80 flex flex-col gap-4 shrink-0">
                <Button variant="secondary" size="sm" className="self-start" onClick={returnToDashboard}>
                  <ChevronLeft size={16} /> Leave Game
                </Button>
                
                <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-200 flex-1 flex flex-col gap-6">
                   {/* Timer */}
                   {match.mode === 'ranked' && (
                     <div className="flex items-center justify-center bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-4 border-2 border-blue-200">
                       <Clock size={24} className="text-blue-600 mr-2" />
                       <div className="text-center">
                         <div className="text-sm font-semibold text-gray-600">Time Left</div>
                         <div className={`text-3xl font-black ${timeLeft <= 10 ? 'text-red-600 animate-pulse' : 'text-blue-600'}`}>
                           {timeLeft}s
                         </div>
                       </div>
                     </div>
                   )}

                   {/* Player Card */}
                   <div className={`p-4 rounded-xl transition-all ${gameState.currentPlayer === 1 ? 'bg-blue-50 ring-2 ring-blue-200' : 'bg-gray-50'}`}>
                      <span className="text-sm font-bold text-gray-400">YOU (X)</span>
                      <div className="font-bold text-xl">{user?.display_name}</div>
                   </div>

                   <div className="flex justify-center items-center">
                      <div className="text-4xl font-black text-gray-300">VS</div>
                   </div>

                   {/* Opponent Card */}
                   <div className={`p-4 rounded-xl transition-all ${gameState.currentPlayer === 2 ? 'bg-pink-50 ring-2 ring-pink-200' : 'bg-gray-50'}`}>
                      <span className="text-sm font-bold text-gray-400">OPPONENT (O)</span>
                      <div className="font-bold text-xl">{match.opponent?.display_name || 'Waiting...'}</div>
                   </div>
                </div>
             </div>

             <div className="flex-1 bg-white rounded-3xl shadow-lg border border-gray-200 flex flex-col relative overflow-hidden">
                {gameState.winner !== 0 && (
                  <div className="absolute inset-0 z-50 bg-black/20 backdrop-blur-sm flex items-center justify-center">
                     <div className="bg-white p-8 rounded-3xl shadow-2xl text-center">
                        <div className="text-6xl mb-4">{gameState.winner === 1 ? '🏆' : (gameState.winner === 'draw' ? '🤝' : '💀')}</div>
                        <h2 className="text-3xl font-black mb-2 text-gray-800">
                          {gameState.winner === 1 ? 'VICTORY!' : (gameState.winner === 'draw' ? 'DRAW' : 'DEFEAT')}
                        </h2>
                        <Button onClick={returnToDashboard}>Back to Hub</Button>
                     </div>
                  </div>
                )}
                
                <div className="flex-1 flex items-center justify-center p-4">
                   <GameBoard 
                     board={gameState.board} 
                     type={match.type} 
                     onCellClick={handleMove}
                     winningLine={gameState.winningLine}
                     lastMove={gameState.lastMove}
                     currentPlayer={gameState.currentPlayer}
                     disabled={gameState.winner !== 0 || (gameState.currentPlayer !== playerNumber)}
                   />
                </div>
             </div>
          </div>
        )}
      </main>

      {/* Rank Info Modals */}
      <RankInfoModal 
        gameType="tic-tac-toe" 
        isOpen={showRankInfo === 'tic-tac-toe'} 
        onClose={() => setShowRankInfo(null)}
      />
      <RankInfoModal 
        gameType="caro" 
        isOpen={showRankInfo === 'caro'} 
        onClose={() => setShowRankInfo(null)}
      />
    </div>
  );
}
