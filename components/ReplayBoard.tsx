import React, { useState, useEffect } from 'react';
import GameBoard from './GameBoard';
import Button from './Button';
import { ArrowLeft, ChevronLeft, ChevronRight, RotateCcw, Play, Pause } from 'lucide-react';
import { CellValue } from '../types';

interface ReplayBoardProps {
    matchData: any; // Dữ liệu lấy từ API /match/:id
    onBack: () => void;
}

const ReplayBoard: React.FC<ReplayBoardProps> = ({ matchData, onBack }) => {
    const [currentStep, setCurrentStep] = useState(0);
    const [boardState, setBoardState] = useState<CellValue[][]>([]);
    const [isPlaying, setIsPlaying] = useState(false);

    // Khởi tạo bàn cờ rỗng dựa trên game_type
    const initBoard = () => {
        const rows = matchData.game_type === 'caro' ? 15 : 3;
        const cols = matchData.game_type === 'caro' ? 20 : 3;
        return Array(rows).fill(null).map(() => Array(cols).fill(0));
    };

    // Tính toán bàn cờ tại bước thứ 'step'
    useEffect(() => {
        const newBoard = initBoard();
        const movesToApply = matchData.moves ? (typeof matchData.moves === 'string' ? JSON.parse(matchData.moves) : matchData.moves).slice(0, currentStep) : [];

        movesToApply.forEach((move: any) => {
            if (newBoard[move.r] && newBoard[move.r][move.c] !== undefined) {
                newBoard[move.r][move.c] = move.player;
            }
        });
        setBoardState(newBoard);
    }, [currentStep, matchData]);

    // Tự động chạy (Auto play)
    useEffect(() => {
        let interval: any;
        if (isPlaying) {
            interval = setInterval(() => {
                setCurrentStep(prev => {
                    const totalMoves = matchData.moves ? (typeof matchData.moves === 'string' ? JSON.parse(matchData.moves) : matchData.moves).length : 0;
                    if (prev >= totalMoves) {
                        setIsPlaying(false);
                        return prev;
                    }
                    return prev + 1;
                });
            }, 1000); // 1 giây 1 nước
        }
        return () => clearInterval(interval);
    }, [isPlaying, matchData]);

    const totalMoves = matchData.moves ? (typeof matchData.moves === 'string' ? JSON.parse(matchData.moves) : matchData.moves).length : 0;

    return (
        <div className="min-h-screen bg-slate-50 flex flex-col items-center p-4">
            <div className="w-full max-w-4xl flex items-center justify-between mb-4">
                <Button variant="secondary" onClick={onBack} size="sm">
                    <ArrowLeft size={16} className="mr-2" /> Quay lại
                </Button>
                <div className="text-center">
                    <h2 className="font-bold text-xl">Replay: {matchData.p1_name} vs {matchData.p2_name}</h2>
                    <p className="text-sm text-gray-500">Nước thứ: {currentStep} / {totalMoves}</p>
                </div>
                <div className="w-24"></div> {/* Spacer */}
            </div>

            {totalMoves === 0 && (
                <div className="w-full max-w-4xl mb-4 bg-yellow-50 border-2 border-yellow-400 rounded-xl p-6 text-center">
                    <p className="text-yellow-800 font-bold text-lg mb-2">⚠️ Không có dữ liệu nước đi</p>
                    <p className="text-yellow-700 text-sm">
                        Trận đấu này không có dữ liệu replay. Điều này xảy ra khi trận đấu được chơi trước khi tính năng replay được cập nhật.
                        <br />
                        Vui lòng chơi một trận mới để xem replay.
                    </p>
                </div>
            )}

            <div className="flex-1 w-full max-w-4xl flex justify-center mb-4">
                <GameBoard
                    board={boardState}
                    type={matchData.game_type}
                    onCellClick={() => { }} // Replay không cho click
                    disabled={true}
                    currentPlayer={1} // Just a dummy value
                    lastMove={null}
                    winningLine={null}
                />
            </div>

            {/* Control Bar */}
            <div className="bg-white p-4 rounded-2xl shadow-lg flex gap-4 items-center">
                <button onClick={() => setCurrentStep(0)} className="p-2 hover:bg-gray-100 rounded-full" title="Về đầu">
                    <RotateCcw size={24} />
                </button>
                <button
                    onClick={() => setCurrentStep(s => Math.max(0, s - 1))}
                    className="p-2 hover:bg-gray-100 rounded-full"
                    disabled={currentStep === 0}
                >
                    <ChevronLeft size={24} />
                </button>

                <button
                    onClick={() => setIsPlaying(!isPlaying)}
                    className={`px-6 py-2 rounded-full font-bold text-white flex items-center gap-2 ${isPlaying ? 'bg-red-500' : 'bg-blue-500'}`}
                >
                    {isPlaying ? <><Pause size={18} /> Tạm dừng</> : <><Play size={18} /> Phát</>}
                </button>

                <button
                    onClick={() => setCurrentStep(s => Math.min(totalMoves, s + 1))}
                    className="p-2 hover:bg-gray-100 rounded-full"
                    disabled={currentStep === totalMoves}
                >
                    <ChevronRight size={24} />
                </button>
            </div>
        </div>
    );
};

export default ReplayBoard;
