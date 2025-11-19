import React from 'react';
import { X, Trophy, TrendingUp } from 'lucide-react';
import Button from './Button';

interface RankInfoModalProps {
  gameType: 'tic-tac-toe' | 'caro';
  isOpen: boolean;
  onClose: () => void;
}

export const RankInfoModal: React.FC<RankInfoModalProps> = ({ gameType, isOpen, onClose }) => {
  if (!isOpen) return null;

  const isTicTacToe = gameType === 'tic-tac-toe';

  const rankInfo = {
    'tic-tac-toe': {
      title: 'Hệ Thống Xếp Hạng Tic-Tac-Toe',
      description: 'Game chiến thuật 3x3 kinh điển',
      winPoints: 25,
      lossPoints: -10,
      ranks: [
        { level: 'Bronze', range: '0-499 pts', color: 'from-amber-600 to-amber-400', description: 'Mức người mới - Vừa bắt đầu chơi' },
        { level: 'Silver', range: '500-999 pts', color: 'from-gray-400 to-gray-200', description: 'Mức trung bình - Đang phát triển kỹ năng' },
        { level: 'Gold', range: '1000-1999 pts', color: 'from-yellow-500 to-yellow-300', description: 'Mức nâng cao - Người chơi mạnh' },
        { level: 'Crystal', range: '2000+ pts', color: 'from-cyan-400 to-blue-300', description: 'Mức cao nhất - Người chơi chuyên nghiệp' }
      ],
      mechanics: [
        'Mỗi lần thắng được +25 điểm xếp hạng',
        'Mỗi lần thua mất -10 điểm xếp hạng',
        'Trận hòa không ảnh hưởng đến xếp hạng',
        'Leo rank để mở khóa các badge độc quyền',
        'Theo dõi tiến độ trên bảng xếp hạng toàn cầu'
      ]
    },
    'caro': {
      title: 'Hệ Thống Xếp Hạng Caro (Gomoku)',
      description: 'Game chiến thuật 15x20 xếp 5 liên tiếp',
      winPoints: 25,
      lossPoints: -10,
      ranks: [
        { level: 'Bronze', range: '0-499 pts', color: 'from-amber-600 to-amber-400', description: 'Mức người mới - Đang học Caro' },
        { level: 'Silver', range: '500-999 pts', color: 'from-gray-400 to-gray-200', description: 'Mức trung bình - Tư duy chiến thuật' },
        { level: 'Gold', range: '1000-1999 pts', color: 'from-yellow-500 to-yellow-300', description: 'Mức nâng cao - Chơi có kế hoạch' },
        { level: 'Crystal', range: '2000+ pts', color: 'from-cyan-400 to-blue-300', description: 'Mức cao nhất - Huyền thoại Caro' }
      ],
      mechanics: [
        'Thắng bằng cách xếp 5 quân liên tiếp (ngang, dọc hoặc chéo)',
        'Mỗi lần thắng được +25 điểm xếp hạng',
        'Mỗi lần thua mất -10 điểm xếp hạng',
        'Trận hòa không ảnh hưởng đến xếp hạng',
        'Cạnh tranh trên bảng xếp hạng toàn cầu'
      ]
    }
  };

  const info = rankInfo[gameType];

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-3xl shadow-lg border border-gray-200 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-gradient-to-r from-blue-500 to-purple-600 text-white p-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Trophy size={28} />
            <div>
              <h2 className="text-2xl font-black">{info.title}</h2>
              <p className="text-blue-100 text-sm">{info.description}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-white/20 rounded-full transition"
          >
            <X size={24} />
          </button>
        </div>

        {/* Content */}
        <div className="p-8 space-y-8">
          {/* Points Info */}
          <div className="bg-blue-50 rounded-2xl p-6">
            <h3 className="font-black text-lg text-gray-800 mb-4 flex items-center gap-2">
              <TrendingUp size={20} className="text-blue-600" />
              Hệ Thống Điểm
            </h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-green-50 rounded-xl p-4 border-l-4 border-green-500">
                <div className="text-sm text-gray-600 font-semibold">Thắng</div>
                <div className="text-3xl font-black text-green-600">+{info.winPoints}</div>
              </div>
              <div className="bg-red-50 rounded-xl p-4 border-l-4 border-red-500">
                <div className="text-sm text-gray-600 font-semibold">Thua</div>
                <div className="text-3xl font-black text-red-600">{info.lossPoints}</div>
              </div>
            </div>
          </div>

          {/* Rank Tiers */}
          <div>
            <h3 className="font-black text-lg text-gray-800 mb-4">Cấp Xếp Hạng</h3>
            <div className="space-y-3">
              {info.ranks.map((rank, idx) => (
                <div key={idx} className="flex items-start gap-4 p-4 rounded-xl hover:bg-gray-50 transition border border-gray-100">
                  <div className={`w-16 h-16 rounded-lg bg-gradient-to-br ${rank.color} flex items-center justify-center text-white font-black text-sm text-center`}>
                    {rank.level}
                  </div>
                  <div className="flex-1">
                    <div className="font-bold text-gray-800">{rank.level}</div>
                    <div className="text-sm text-gray-600">{rank.range}</div>
                    <div className="text-xs text-gray-500 mt-1">{rank.description}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Game Mechanics */}
          <div>
            <h3 className="font-black text-lg text-gray-800 mb-4">Cách Thức Hoạt Động</h3>
            <ul className="space-y-2">
              {info.mechanics.map((mechanic, idx) => (
                <li key={idx} className="flex items-start gap-3 p-3 rounded-lg bg-gray-50">
                  <div className="w-6 h-6 rounded-full bg-blue-500 text-white flex items-center justify-center flex-shrink-0 text-xs font-bold">
                    {idx + 1}
                  </div>
                  <span className="text-gray-700">{mechanic}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Tips */}
          <div className="bg-yellow-50 rounded-2xl p-6 border-l-4 border-yellow-400">
            <h3 className="font-black text-gray-800 mb-3">💡 Mẹo Chơi</h3>
            <ul className="space-y-2 text-sm text-gray-700">
              <li>• Chơi thường xuyên để leo rank nhanh hơn</li>
              <li>• Chế độ luyện tập không ảnh hưởng đến xếp hạng</li>
              <li>• Học hỏi từ những người chơi hàng đầu</li>
              <li>• Cố gắng giữ chuỗi thắng liên tiếp</li>
            </ul>
          </div>
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-white border-t border-gray-200 p-6">
          <Button onClick={onClose} className="w-full">
            Đã Hiểu!
          </Button>
        </div>
      </div>
    </div>
  );
};

export default RankInfoModal;
