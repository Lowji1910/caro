import React from 'react';
import { GameType, GameLevel } from '../types';
import { ArrowLeft, Zap, Flame, Crown } from 'lucide-react';
import Button from './Button';

interface LevelSelectorProps {
  gameType: GameType;
  onSelectLevel: (level: GameLevel) => void;
  onBack: () => void;
}

const LevelSelector: React.FC<LevelSelectorProps> = ({ gameType, onSelectLevel, onBack }) => {
  const levels: { level: GameLevel; title: string; description: string; icon: React.ReactNode; color: string; bgColor: string }[] = [
    {
      level: 'beginner',
      title: '🌱 Beginner',
      description: 'Perfect for newcomers. Take your time and learn the basics.',
      icon: <Zap size={24} />,
      color: 'from-green-400 to-emerald-500',
      bgColor: 'bg-green-50'
    },
    {
      level: 'intermediate',
      title: '⚡ Intermediate',
      description: 'Moderate difficulty. You know the rules, now challenge yourself.',
      icon: <Flame size={24} />,
      color: 'from-orange-400 to-red-500',
      bgColor: 'bg-orange-50'
    },
    {
      level: 'advanced',
      title: '🔥 Advanced',
      description: 'High difficulty. Strategic thinking required. Fast pace.',
      icon: <Flame size={24} />,
      color: 'from-red-500 to-pink-600',
      bgColor: 'bg-red-50'
    },
    {
      level: 'expert',
      title: '👑 Expert',
      description: 'Extreme difficulty. AI plays at the highest level. Ultra-fast.',
      icon: <Crown size={24} />,
      color: 'from-purple-500 to-indigo-600',
      bgColor: 'bg-purple-50'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 shadow-md sticky top-0 z-40">
        <div className="container mx-auto px-4 py-6 flex items-center gap-4">
          <button 
            onClick={onBack} 
            className="flex items-center gap-2 text-blue-600 hover:text-blue-800 font-semibold transition-colors"
          >
            <ArrowLeft size={20} /> Back
          </button>
          <div>
            <h1 className="text-3xl font-black text-gray-800">
              {gameType === 'tic-tac-toe' ? '🎮 Tic-Tac-Toe' : '● Caro'} - Choose Level
            </h1>
            <p className="text-gray-500 text-sm">Select your difficulty level to begin</p>
          </div>
        </div>
      </div>

      {/* Content */}
      <main className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-5xl mx-auto">
          {levels.map((level) => (
            <button
              key={level.level}
              onClick={() => onSelectLevel(level.level)}
              className="group text-left"
            >
              <div className={`${level.bgColor} rounded-2xl p-6 border-2 border-gray-200 shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-200 h-full`}>
                {/* Icon and Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className={`bg-gradient-to-br ${level.color} text-white p-4 rounded-xl shadow-lg group-hover:scale-110 transition-transform`}>
                    {level.icon}
                  </div>
                  <div className="text-right">
                    <span className={`inline-block bg-gradient-to-r ${level.color} text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider`}>
                      {level.level === 'beginner' ? '⭐ Easy' : level.level === 'intermediate' ? '⭐⭐ Medium' : level.level === 'advanced' ? '⭐⭐⭐ Hard' : '⭐⭐⭐⭐ Extreme'}
                    </span>
                  </div>
                </div>

                {/* Title */}
                <h2 className="text-2xl font-black text-gray-800 mb-2">
                  {level.title}
                </h2>

                {/* Description */}
                <p className="text-gray-600 text-sm mb-6 leading-relaxed">
                  {level.description}
                </p>

                {/* Stats */}
                <div className="grid grid-cols-3 gap-3 mb-6 pt-4 border-t border-gray-300">
                  <div className="text-center">
                    <div className={`text-2xl font-black bg-gradient-to-r ${level.color} bg-clip-text text-transparent`}>
                      {level.level === 'beginner' ? '30s' : level.level === 'intermediate' ? '20s' : level.level === 'advanced' ? '10s' : '5s'}
                    </div>
                    <div className="text-xs text-gray-500 font-semibold">Per Turn</div>
                  </div>
                  <div className="text-center">
                    <div className={`text-2xl font-black bg-gradient-to-r ${level.color} bg-clip-text text-transparent`}>
                      {level.level === 'beginner' ? '+15' : level.level === 'intermediate' ? '+20' : level.level === 'advanced' ? '+25' : '+35'}
                    </div>
                    <div className="text-xs text-gray-500 font-semibold">Win Points</div>
                  </div>
                  <div className="text-center">
                    <div className={`text-2xl font-black bg-gradient-to-r ${level.color} bg-clip-text text-transparent`}>
                      {level.level === 'beginner' ? '-5' : level.level === 'intermediate' ? '-10' : level.level === 'advanced' ? '-15' : '-25'}
                    </div>
                    <div className="text-xs text-gray-500 font-semibold">Lose Points</div>
                  </div>
                </div>

                {/* Play Button */}
                <Button 
                  className={`w-full bg-gradient-to-r ${level.color} text-white border-0`}
                  onClick={() => onSelectLevel(level.level)}
                >
                  Play {level.title}
                </Button>
              </div>
            </button>
          ))}
        </div>

        {/* Tips Section */}
        <div className="mt-12 bg-white rounded-2xl p-6 border border-gray-200 shadow-lg max-w-3xl mx-auto">
          <h3 className="text-xl font-black text-gray-800 mb-4">💡 Tips for Choosing Your Level</h3>
          <ul className="space-y-3 text-gray-700">
            <li className="flex items-start gap-3">
              <span className="flex-shrink-0 w-6 h-6 bg-green-100 text-green-700 rounded-full flex items-center justify-center text-xs font-bold">1</span>
              <span><strong>Beginner:</strong> Start here if you're new to the game or want to relax</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="flex-shrink-0 w-6 h-6 bg-orange-100 text-orange-700 rounded-full flex items-center justify-center text-xs font-bold">2</span>
              <span><strong>Intermediate:</strong> You understand the game mechanics and want a fair challenge</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="flex-shrink-0 w-6 h-6 bg-red-100 text-red-700 rounded-full flex items-center justify-center text-xs font-bold">3</span>
              <span><strong>Advanced:</strong> You're competitive and looking for strategic gameplay</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="flex-shrink-0 w-6 h-6 bg-purple-100 text-purple-700 rounded-full flex items-center justify-center text-xs font-bold">4</span>
              <span><strong>Expert:</strong> Ultimate challenge - only for the most skilled players!</span>
            </li>
          </ul>
        </div>
      </main>
    </div>
  );
};

export default LevelSelector;
