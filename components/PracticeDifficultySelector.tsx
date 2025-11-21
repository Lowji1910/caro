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
    <div className="min-h-screen bg-gradient-to-b from-sky-50 via-white to-slate-50 text-slate-900">
      <div className="max-w-6xl mx-auto px-4 py-12 space-y-10">
        <div className="bg-white shadow-2xl shadow-slate-200 rounded-3xl border border-slate-100 p-8 flex flex-col gap-6">
          <div className="flex items-center gap-3">
            <button
              onClick={onBack}
              className="rounded-full border border-slate-200 bg-white p-2 text-slate-600 hover:text-slate-900 transition-shadow shadow-sm"
            >
              <ArrowLeft size={20} />
            </button>
            <div>
              <p className="text-xs uppercase tracking-[0.4em] text-slate-500">Luyện tập</p>
              <h1 className="text-4xl md:text-5xl font-black leading-tight text-slate-900">
                {gameLabel} <span className="text-sky-600">• Chọn độ khó</span>
              </h1>
              <p className="text-slate-500 mt-1">Tinh chỉnh phản xạ và chiến thuật trước khi bước vào trận đấu xếp hạng.</p>
            </div>
          </div>
          {isProcessing && (
            <div className="flex items-start gap-3 rounded-2xl border border-slate-200 bg-slate-50 p-4 text-slate-600">
              <Activity size={20} className="mt-1 animate-spin" />
              <div>
                <p className="font-semibold text-slate-800">Đang thiết lập trận luyện tập...</p>
                <p className="text-sm text-slate-500">Bạn sẽ được chuyển vào bàn đấu ngay khi AI sẵn sàng.</p>
              </div>
            </div>
          )}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-slate-50 rounded-2xl border border-slate-100 p-4 flex flex-col gap-3">
              <div className="flex items-center gap-2 text-slate-400">
                <Shield size={18} />
                <p className="text-xs uppercase tracking-[0.3em]">Tốc độ phản ứng</p>
              </div>
              <p className="text-xl font-bold text-slate-900">Tuỳ chỉnh linh hoạt</p>
              <p className="text-sm text-slate-500">Từ dễ đến khó, AI phản hồi nhanh hơn từng bước một.</p>
            </div>
            <div className="bg-slate-50 rounded-2xl border border-slate-100 p-4 flex flex-col gap-3">
              <div className="flex items-center gap-2 text-slate-400">
                <Zap size={18} />
                <p className="text-xs uppercase tracking-[0.3em]">Khả năng học</p>
              </div>
              <p className="text-xl font-bold text-slate-900">Thuật toán tinh chỉnh</p>
              <p className="text-sm text-slate-500">Theo dõi mẫu chiến thuật và đánh giá tình huống thực.</p>
            </div>
            <div className="bg-slate-50 rounded-2xl border border-slate-100 p-4 flex flex-col gap-3">
              <div className="flex items-center gap-2 text-slate-400">
                <Activity size={18} />
                <p className="text-xs uppercase tracking-[0.3em]">Từ vựng chiến thuật</p>
              </div>
              <p className="text-xl font-bold text-slate-900">Tăng tiến trải nghiệm</p>
              <p className="text-sm text-slate-500">Mỗi độ khó là nấc thang để bạn nâng cao kỹ năng.</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {difficultyOptions.map(diff => (
            <div
              key={diff.value}
              className="relative overflow-hidden rounded-3xl border border-slate-200 bg-white p-6 shadow-lg shadow-slate-200"
            >
              <div className="relative flex items-center justify-between">
                <div>
                  <span className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold tracking-[0.2em] uppercase text-white ${diff.gradient}`}>{diff.subLabel}</span>
                  <h2 className="mt-5 text-3xl font-black flex items-center gap-2 text-slate-900">
                    {diff.label}
                    <span className="text-slate-400 text-sm font-medium">({gameLabel})</span>
                  </h2>
                  <p className="text-sm text-slate-500 mt-3 leading-relaxed">{diff.description}</p>
                </div>
                <div className={`rounded-2xl border ${diff.accent} border-current px-3 py-2 text-xs font-semibold uppercase`}>AI {diff.label}</div>
              </div>

              <p className="mt-4 text-slate-500 text-sm italic">{diff.highlight}</p>

              <div className="mt-5 space-y-2">
                {diff.insights.map(insight => (
                  <div key={insight} className="flex items-center gap-3 text-sm text-slate-600">
                    <span className="text-slate-400"><Activity size={16} /></span>
                    <span>{insight}</span>
                  </div>
                ))}
              </div>

              <Button
                className={`mt-6 w-full bg-gradient-to-r ${diff.gradient} text-white`}
                onClick={() => onSelect(diff.value)}
                disabled={isProcessing}
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
