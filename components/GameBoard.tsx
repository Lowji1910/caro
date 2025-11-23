import React, { useEffect, useRef } from 'react';
import { CellValue, GameType, PlayerId } from '../types';
import { Focus } from 'lucide-react';
import { COLORS } from '../constants';

interface GameBoardProps {
  board: CellValue[][];
  type: GameType;
  onCellClick: (r: number, c: number) => void;
  winningLine: { r: number; c: number }[] | null;
  lastMove: { r: number; c: number } | null;
  currentPlayer: PlayerId;
  disabled: boolean;
  onUndo?: () => void;
}

const GameBoard: React.FC<GameBoardProps> = ({
  board,
  type,
  onCellClick,
  winningLine,
  lastMove,
  disabled,
  onUndo
}) => {
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const isTicTacToe = type === 'tic-tac-toe';

  const [isDragging, setIsDragging] = React.useState(false);
  const [dragStart, setDragStart] = React.useState({ x: 0, y: 0, scrollLeft: 0, scrollTop: 0 });
  const [hasDragged, setHasDragged] = React.useState(false);

  useEffect(() => {
    if (!isTicTacToe && scrollContainerRef.current) {
      const container = scrollContainerRef.current;
      container.scrollTop = (container.scrollHeight - container.clientHeight) / 2;
      container.scrollLeft = (container.scrollWidth - container.clientWidth) / 2;
    }
  }, [isTicTacToe, board]);

  // --- SAFETY CHECK QUAN TRỌNG ---
  // Nếu board chưa tải xong hoặc null, không render gì cả để tránh crash
  if (!board || board.length === 0 || !board[0]) {
    return (
      <div className="flex items-center justify-center h-64 w-full text-gray-400 animate-pulse">
        Loading board...
      </div>
    );
  }

  const handleCenter = () => {
    if (scrollContainerRef.current) {
      const container = scrollContainerRef.current;
      container.scrollTo({
        top: (container.scrollHeight - container.clientHeight) / 2,
        left: (container.scrollWidth - container.clientWidth) / 2,
        behavior: 'smooth'
      });
    }
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    if (isTicTacToe || !scrollContainerRef.current) return;
    setIsDragging(true);
    setHasDragged(false);
    setDragStart({
      x: e.pageX,
      y: e.pageY,
      scrollLeft: scrollContainerRef.current.scrollLeft,
      scrollTop: scrollContainerRef.current.scrollTop
    });
    // Change cursor to grabbing
    scrollContainerRef.current.style.cursor = 'grabbing';
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDragging || !scrollContainerRef.current) return;
    e.preventDefault();
    const x = e.pageX - dragStart.x;
    const y = e.pageY - dragStart.y;

    // If moved more than 5px, consider it a drag action (prevent click)
    if (Math.abs(x) > 5 || Math.abs(y) > 5) {
      setHasDragged(true);
    }

    scrollContainerRef.current.scrollLeft = dragStart.scrollLeft - x;
    scrollContainerRef.current.scrollTop = dragStart.scrollTop - y;
  };

  const handleMouseUp = () => {
    setIsDragging(false);
    if (scrollContainerRef.current) {
      scrollContainerRef.current.style.cursor = 'default';
    }
  };

  const handleMouseLeave = () => {
    setIsDragging(false);
    if (scrollContainerRef.current) {
      scrollContainerRef.current.style.cursor = 'default';
    }
  };

  const renderCell = (r: number, c: number, value: CellValue) => {
    const isWinningCell = winningLine?.some(pos => pos.r === r && pos.c === c);
    const isLastMove = lastMove?.r === r && lastMove?.c === c;

    let content = null;
    if (value === 1) { // X
      content = (
        <svg viewBox="0 0 24 24" className="w-full h-full p-1 sm:p-2 drop-shadow-sm" style={{ color: COLORS.primaryPink }}>
          <path fill="currentColor" d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" />
        </svg>
      );
    } else if (value === 2) { // O
      content = (
        <svg viewBox="0 0 24 24" className="w-full h-full p-1 sm:p-2 drop-shadow-sm" style={{ color: COLORS.primaryBlue }}>
          <path fill="currentColor" d="M12 2C6.47 2 2 6.47 2 12s4.47 10 10 10 10-4.47 10-10S17.53 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z" />
        </svg>
      );
    }

    const cellBaseClass = `
      relative flex items-center justify-center cursor-pointer 
      transition-all duration-200 select-none
      ${isTicTacToe ? 'rounded-2xl text-5xl' : 'rounded-md text-xl border border-gray-400'}
      ${value === 0 && !disabled ? 'hover:bg-white/80 hover:shadow-md' : ''}
      ${isWinningCell ? 'bg-yellow-200 ring-3 ring-yellow-400 z-10 scale-105 shadow-lg' : ''}
      ${!isWinningCell && isLastMove ? 'bg-blue-100 ring-3 ring-blue-400 z-10 shadow-md' : 'bg-white'}
    `;

    return (
      <div
        key={`${r}-${c}`}
        onClick={() => !disabled && value === 0 && !hasDragged && onCellClick(r, c)}
        className={cellBaseClass}
        style={{
          boxShadow: isTicTacToe ? '0 6px 12px -2px rgba(0, 0, 0, 0.15)' : 'inset 0 0 0 1px rgba(0,0,0,0.1)',
          width: isTicTacToe ? '100%' : '40px',
          height: isTicTacToe ? '100%' : '40px'
        }}
      >
        {content}
      </div>
    );
  };

  if (isTicTacToe) {
    return (
      <div className="relative w-full max-w-[450px] mx-auto">
        <div className="absolute -top-12 right-0 flex gap-2 z-20">
          {onUndo && (
            <button
              onClick={onUndo}
              className="p-2 bg-white rounded-full shadow-lg hover:bg-gray-50 text-red-500 border border-gray-300 transition-all hover:scale-110 disabled:opacity-50 disabled:cursor-not-allowed"
              title="Undo Request"
            >
              <span className="font-bold text-lg">↩</span>
            </button>
          )}
        </div>
        <div className="aspect-square w-full grid grid-cols-3 grid-rows-3 gap-4 p-4 bg-gradient-to-br from-blue-50 to-purple-50 rounded-3xl shadow-xl border border-gray-300">
          {board.map((row, r) => row.map((val, c) => renderCell(r, c, val)))}
        </div>
      </div>
    );
  }

  // Caro Board
  return (
    <div className="relative w-full h-full flex flex-col items-center justify-center min-h-[300px]">
      <div className="absolute top-4 right-4 flex flex-col gap-2 z-20">
        <button onClick={handleCenter} className="p-3 bg-white rounded-full shadow-lg hover:bg-gray-50 text-blue-600 border border-gray-300 transition-all hover:scale-110">
          <Focus size={20} />
        </button>
        {onUndo && (
          <button
            onClick={onUndo}
            className="p-3 bg-white rounded-full shadow-lg hover:bg-gray-50 text-red-500 border border-gray-300 transition-all hover:scale-110 disabled:opacity-50 disabled:cursor-not-allowed"
            title="Undo Request"
          >
            <span className="font-bold text-lg">↩</span>
          </button>
        )}
      </div>

      <div
        ref={scrollContainerRef}
        className="overflow-auto w-full h-full border-4 border-gray-400 bg-[#fdf6e3] shadow-lg rounded-2xl no-scrollbar relative cursor-grab active:cursor-grabbing"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseLeave}
        style={{
          backgroundImage: 'radial-gradient(#c9a961 1.5px, transparent 1.5px)',
          backgroundSize: '24px 24px',
          maxHeight: '70vh'
        }}
      >
        <div
          className="grid p-8 mx-auto bg-[#fdf6e3]"
          style={{
            gridTemplateColumns: `repeat(${board[0].length}, 40px)`,
            width: 'fit-content',
            gap: '0px'
          }}
        >
          {board.map((row, r) => row.map((val, c) => renderCell(r, c, val)))}
        </div>
      </div>
    </div>
  );
};

export default GameBoard;