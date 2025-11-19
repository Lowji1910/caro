import React from 'react';
import { ArrowLeft } from 'lucide-react';
import { GameType, AIDifficulty } from '../types';
import Button from './Button';

interface PracticeDifficultySelectorProps {
  gameType: GameType;
  onSelect: (difficulty: AIDifficulty) => void;
  onBack: () => void;
}

const difficultyOptions: { value: AIDifficulty; label: string; subLabel: string; description: string; gradient: string }[] = [
  {
    value: 'easy',
    label: 'Dễ',
    subLabel: 'Relaxed',
    description: 'Lưu ý vừa đủ để làm quen với nhịp chơi.',
    gradient: 'from-emerald-400 to-emerald-600'
  },
  {
    value: 'medium',
    label: 'Trung bình',
    subLabel: 'Balanced',
    description: 'Thử thách vừa phải, vẫn có thể kiểm soát tình huống.',
    gradient: 'from-orange-400 to-rose-500'
  },
  {
    value: 'hard',
    label: 'Khó',
    subLabel: 'Hardcore',
    description: 'AI phản ứng nhanh, thích hợp luyện chiến thuật.',
    gradient: 'from-fuchsia-500 to-violet-600'
  }
];

const PracticeDifficultySelector: React.FC<PracticeDifficultySelectorProps> = ({ gameType, onSelect, onBack }) => {
  const gameLabel = gameType === 'tic-tac-toe' ? 'Tic-Tac-Toe' : 'Caro';

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <div className="max-w-5xl mx-auto px-4 py-8">
        <div className="flex items-center gap-3 mb-6">
          <button
            onClick={onBack}
            className="flex items-center gap-2 text-slate-200 hover:text-white font-semibold"
          >
            <ArrowLeft size={20} /> Quay lại
          </button>
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-slate-400">Luyện tập</p>
            <h1 className="text-3xl font-black">{gameLabel} • Chọn độ khó</h1>
            <p className="text-slate-300 text-sm">Tùy theo mục tiêu luyện tập bạn hãy chọn tốc độ và phản ứng AI phù hợp.</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {difficultyOptions.map(diff => (
            <div key={diff.value} className="bg-white/5 rounded-3xl border border-white/10 shadow-lg p-6 flex flex-col justify-between">
              <div>
                <div className={`inline-flex px-3 py-1 rounded-full text-xs font-bold uppercase tracking-[0.2em] bg-gradient-to-r ${diff.gradient}`}>{diff.subLabel}</div>
                <h2 className="mt-4 text-2xl font-black text-white flex items-baseline gap-2">
                  {diff.label}
                  <span className="text-slate-400 text-sm font-medium">({gameLabel})</span>
                </h2>
                <p className="text-slate-300 mt-3 text-sm leading-relaxed">{diff.description}</p>
              </div>
              <Button
                className={`mt-6 w-full bg-gradient-to-r ${diff.gradient} text-white`}
                onClick={() => onSelect(diff.value)}
              >
                Bắt đầu {diff.label}
              </Button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PracticeDifficultySelector;
