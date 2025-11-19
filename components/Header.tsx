
import React from 'react';
import { UserProfile } from '../types';
import { LogOut, User as UserIcon } from 'lucide-react';
import { COLORS } from '../constants';
import { getTierInfo } from '../utils/tierUtils';
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
        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white font-bold text-lg shadow-inner">
          {user.display_name?.charAt(0)?.toUpperCase() || 'U'}
        </div>
        <div className="hidden sm:block">
          <div className="flex items-center gap-2">
            <h1 className="font-bold text-gray-800 text-lg leading-tight">{user.display_name}</h1>
            {tierInfo && (
              <span 
                className="px-3 py-1 rounded-full text-white text-xs font-bold uppercase tracking-wider shadow-md"
                style={{ backgroundColor: tierInfo.color }}
              >
                {tierInfo.name}
              </span>
            )}
          </div>
          <div className="flex items-center gap-2 text-xs text-gray-500 font-medium mt-1">
            <span className={`px-2 py-0.5 rounded-full text-white shadow-sm text-[10px] uppercase tracking-wider`} 
                  style={{ backgroundColor: COLORS.primaryBlue }}>
              {user.rank_level}
            </span>
            {user.user_level && (
              <span className="text-gray-600 font-semibold">Lv {user.user_level}</span>
            )}
            <span>{user.rank_score} pts</span>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-2 sm:gap-4">
        <Button variant="ghost" size="sm" onClick={onProfile} className="!p-2" title="My Profile">
           <UserIcon size={20} />
        </Button>
        <Button variant="ghost" size="sm" onClick={onLogout} className="!p-2 text-red-400 hover:bg-red-50" title="Logout">
           <LogOut size={20} />
        </Button>
      </div>
    </header>
  );
};

export default Header;
