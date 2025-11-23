import React from 'react';
import { Activity, ArrowLeft, Shield, Zap } from 'lucide-react';
import { GameType, AIDifficulty } from '../types';
import Button from './Button';

interface PracticeDifficultySelectorProps {
  gameType: GameType;
  onSelect: (difficulty: AIDifficulty) => void;
  onBack: () => void;
  isProcessing?: boolean;
}

interface DifficultyOption {
  value: AIDifficulty;
  label: string;
  subLabel: string;
  description: string;
  highlight: string;
  gradient: string;
  accent: string;
  insights: string[];
}

const difficultyOptions: DifficultyOption[] = [
  {
    value: 'easy',
    label: 'Dễ',
    subLabel: 'Relaxed Flow',
    description: 'Tối ưu để phân tích board và huấn luyện phản xạ cơ bản.',
    highlight: 'Chậm rãi, làm quen với nhịp chơi và ghi nhớ cổ điển.',
    gradient: 'from-emerald-400 to-emerald-600',
    accent: 'bg-emerald-500/15 text-emerald-200',
    insights: ['Phản ứng AI: ~800ms', 'Gợi ý tối ưu: Dễ nhận diện', 'Hỗ trợ mở rộng vùng chiến thuật']
  },
  {
    value: 'medium',
    label: 'Trung bình',
    subLabel: 'Balanced Tempo',
    description: 'Cân bằng giữa tốc độ và chiến lược, thích hợp rèn kỹ năng cầm phím.',
    highlight: 'AI bắt đầu bắt bài, phù hợp luyện kiểm soát rủi ro.',
    gradient: 'from-orange-400 to-rose-500',
    accent: 'bg-orange-400/15 text-orange-200',
    insights: ['Phản ứng AI: ~450ms', 'Phát hiện cửa thắng: 3-4 nước', 'Tăng tốc thế trận đều đặn']
  },
  {
    value: 'hard',
    label: 'Khó',
    subLabel: 'Hardcore Clutch',
    description: 'AI phản xạ như đấu thủ chuyên nghiệp, phù hợp chuẩn bị giải đấu.',
    highlight: 'Tốc độ cao, buộc bạn ra quyết định gọn lẹ trong thời gian ngắn.',
    gradient: 'from-fuchsia-500 to-violet-600',
    accent: 'bg-fuchsia-500/15 text-fuchsia-200',
    insights: ['Phản ứng AI: ~250ms', 'Tìm mọi chiêu bài cấm', 'Cải thiện phản xạ và tập trung cao độ']
  }
];

const PracticeDifficultySelector: React.FC<PracticeDifficultySelectorProps> = ({ gameType, onSelect, onBack, isProcessing = false }) => {
  const gameLabel = gameType === 'tic-tac-toe' ? 'Tic-Tac-Toe' : 'Caro';

  return (
    <div className="min-h-screen bg-[#f8fafc] text-slate-900 relative overflow-hidden">
      {/* Background Decor */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none">
        <div className="absolute top-[-20%] right-[-10%] w-[60%] h-[60%] bg-blue-100/50 rounded-full blur-[120px]" />
        <div className="absolute bottom-[-10%] left-[-10%] w-[50%] h-[50%] bg-purple-100/50 rounded-full blur-[120px]" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 py-12 md:py-20 space-y-12">
        {/* Header Section */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
          <div className="space-y-4">
            <button
              onClick={onBack}
              className="group flex items-center gap-2 text-slate-500 hover:text-blue-600 transition-colors font-medium"
            >
              <div className="p-2 rounded-xl bg-white border border-slate-200 shadow-sm group-hover:shadow-md transition-all">
                <ArrowLeft size={20} />
              </div>
              <span>Back to Dashboard</span>
            </button>

            <div>
              <div className="flex items-center gap-3 mb-2">
                <span className="px-3 py-1 rounded-full bg-blue-100 text-blue-700 text-xs font-bold uppercase tracking-wider">
                  Practice Mode
                </span>
                <span className="text-slate-400">•</span>
                <span className="text-slate-500 font-medium">{gameLabel}</span>
              </div>
              <h1 className="text-4xl md:text-6xl font-black text-slate-900 tracking-tight">
                Choose Your <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
                  Challenge Level
                </span>
              </h1>
            </div>
          </div>

          <div className="max-w-md text-slate-600 text-lg leading-relaxed">
            Select an AI difficulty to hone your skills. Each level is designed to simulate different playstyles and strategic depths.
          </div>
        </div>

        {isProcessing && (
          <div className="w-full bg-blue-50 border border-blue-100 rounded-2xl p-6 flex items-center justify-center gap-4 animate-pulse">
            <Activity className="text-blue-600 animate-spin" />
            <span className="text-blue-800 font-semibold">Initializing Practice Match...</span>
          </div>
        )}

        {/* Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {difficultyOptions.map((diff) => (
            <div
              key={diff.value}
              className="group relative bg-white rounded-[32px] border border-slate-100 shadow-xl shadow-slate-200/50 hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-500 overflow-hidden flex flex-col"
            >
              {/* Card Header Gradient */}
              <div className={`h-2 bg-gradient-to-r ${diff.gradient}`} />

              <div className="p-8 flex-1 flex flex-col">
                <div className="flex justify-between items-start mb-6">
                  <div className={`w-14 h-14 rounded-2xl ${diff.accent} flex items-center justify-center text-2xl shadow-inner`}>
                    {diff.value === 'easy' && '🌱'}
                    {diff.value === 'medium' && '⚔️'}
                    {diff.value === 'hard' && '🔥'}
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${diff.accent}`}>
                    {diff.subLabel}
                  </span>
                </div>

                <h3 className="text-3xl font-black text-slate-900 mb-3 group-hover:text-blue-600 transition-colors">
                  {diff.label}
                </h3>

                <p className="text-slate-500 leading-relaxed mb-8">
                  {diff.description}
                </p>

                <div className="space-y-4 mb-8 flex-1">
                  {diff.insights.map((insight, i) => (
                    <div key={i} className="flex items-start gap-3">
                      <div className={`mt-1 w-5 h-5 rounded-full flex items-center justify-center shrink-0 ${diff.accent}`}>
                        <Zap size={10} />
                      </div>
                      <span className="text-sm text-slate-600 font-medium">{insight}</span>
                    </div>
                  ))}
                </div>

                <Button
                  className={`w-full py-4 text-lg font-bold rounded-2xl shadow-lg transition-transform active:scale-[0.98] bg-gradient-to-r ${diff.gradient} text-white border-none hover:brightness-110`}
                  onClick={() => onSelect(diff.value)}
                  disabled={isProcessing}
                >
                  Start {diff.label} Match
                </Button>
              </div>

              {/* Hover Effect Overlay */}
              <div className={`absolute inset-0 bg-gradient-to-r ${diff.gradient} opacity-0 group-hover:opacity-[0.03] transition-opacity duration-500 pointer-events-none`} />
            </div>
          ))}
        </div>

        {/* Footer Info */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-8 border-t border-slate-200">
          <div className="flex items-center gap-4 p-4 rounded-2xl bg-white border border-slate-100 shadow-sm">
            <div className="p-3 rounded-xl bg-green-100 text-green-600">
              <Shield size={24} />
            </div>
            <div>
              <h4 className="font-bold text-slate-900">Safe Environment</h4>
              <p className="text-sm text-slate-500">No rank points lost</p>
            </div>
          </div>
          <div className="flex items-center gap-4 p-4 rounded-2xl bg-white border border-slate-100 shadow-sm">
            <div className="p-3 rounded-xl bg-blue-100 text-blue-600">
              <Activity size={24} />
            </div>
            <div>
              <h4 className="font-bold text-slate-900">Real-time Analysis</h4>
              <p className="text-sm text-slate-500">Instant move feedback</p>
            </div>
          </div>
          <div className="flex items-center gap-4 p-4 rounded-2xl bg-white border border-slate-100 shadow-sm">
            <div className="p-3 rounded-xl bg-purple-100 text-purple-600">
              <Zap size={24} />
            </div>
            <div>
              <h4 className="font-bold text-slate-900">Adaptive AI</h4>
              <p className="text-sm text-slate-500">Learns from your style</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PracticeDifficultySelector;
