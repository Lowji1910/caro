
import React from 'react';
import { UserProfile } from '../types';
import { LogOut, User as UserIcon } from 'lucide-react';
import { COLORS } from '../constants';
import { getTierInfo } from '../utils/tierUtils';
import { getLevelProgress, getRankProgress } from '../utils/levelUtils';
import Button from './Button';

interface HeaderProps {
  user: UserProfile;
  onLogout: () => void;
  onProfile: () => void;
}

const Header: React.FC<HeaderProps> = ({ user, onLogout, onProfile }) => {
  const tierInfo = user.user_level ? getTierInfo(user.user_level) : null;

  return (
    <header className="w-full bg-white/95 backdrop-blur-md shadow-md sticky top-0 z-50 px-4 py-3 flex justify-between items-center border-b border-gray-200">
      <div className="flex items-center gap-3">
        {user.avatar_url ? (
          <img
            src={user.avatar_url}
            alt={user.display_name}
            className="w-10 h-10 rounded-full object-cover shadow-inner border-2 border-white"
            onError={(e) => {
              // Fallback to initial if image fails
              e.currentTarget.style.display = 'none';
              const fallback = e.currentTarget.nextElementSibling as HTMLElement;
              if (fallback) fallback.style.display = 'flex';
            }}
          />
        ) : null}
        <div
          className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white font-bold text-lg shadow-inner"
          style={user.avatar_url ? { display: 'none' } : {}}
        >
          {user.display_name?.charAt(0)?.toUpperCase() || 'U'}
        </div>
        <div className="hidden sm:block">
          <div className="flex flex-col items-end">
            <div className="flex items-center gap-2 mb-1">
              <h1 className="font-bold text-gray-800 text-lg leading-tight">{user.display_name}</h1>
              {tierInfo && (
                <span
                  className="px-2 py-0.5 rounded-full text-white text-[10px] font-bold uppercase tracking-wider shadow-sm"
                  style={{ backgroundColor: tierInfo.color }}
                >
                  {tierInfo.name}
                </span>
              )}
              <span className={`px-2 py-0.5 rounded-full text-white shadow-sm text-[10px] uppercase tracking-wider`}
                style={{ backgroundColor: COLORS.primaryBlue }}>
                {getRankProgress(user.rank_score || 0).rank}
              </span>
            </div>

            <div className="flex items-center gap-3 text-xs font-medium w-full justify-end">
              <span className="text-gray-600 font-bold">Lv {user.user_level || 1}</span>

              {/* Level Progress Bar */}
              <div className="w-24 h-2 bg-gray-100 rounded-full overflow-hidden border border-gray-200 relative group" title={`XP: ${user.xp || 0}`}>
                <div
                  className="h-full bg-green-500 rounded-full transition-all duration-500"
                  style={{ width: `${getLevelProgress(user.xp || 0, user.user_level || 1).percent}%` }}
                />
              </div>

              <span className="text-blue-600 font-bold">{user.rank_score || 0} pts</span>
            </div>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-2 sm:gap-4">
        <Button variant="ghost" size="sm" onClick={onProfile} className="!p-2" title="Hồ sơ của tôi">
          <UserIcon size={20} />
        </Button>
        <Button variant="ghost" size="sm" onClick={onLogout} className="!p-2 text-red-400 hover:bg-red-50" title="Đăng xuất">
          <LogOut size={20} />
        </Button>
      </div>
    </header>
  );
};

export default Header;
