import React, { useState, useEffect } from 'react';
import { UserProfile, MatchHistory } from '../types';
import { ArrowLeft, Edit2, Lock, Eye } from 'lucide-react';
import { COLORS } from '../constants';
import { getTierInfo } from '../utils/tierUtils';
import Button from './Button';

interface ProfileProps {
  user: UserProfile;
  onBack: () => void;
  onUpdate: (updated: Partial<UserProfile>) => Promise<void>;
  onLogout: () => void;
  socketURL: string;
  isPublicView?: boolean;
  onReplayMatch?: (matchId: number) => void;
}

export const Profile: React.FC<ProfileProps> = ({
  user,
  onBack,
  onUpdate,
  onLogout,
  socketURL,
  isPublicView,
  onReplayMatch
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [showPasswordModal, setShowPasswordModal] = useState(false);
  const [matchHistory, setMatchHistory] = useState<MatchHistory[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // Form states
  const [formData, setFormData] = useState<Partial<UserProfile>>({
    full_name: user.full_name || '',
    display_name: user.display_name || '',
    date_of_birth: user.date_of_birth || '',
    bio: user.bio || '',
    avatar_url: user.avatar_url || ''
  });

  const [passwordForm, setPasswordForm] = useState({
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  });

  useEffect(() => {
    fetchMatchHistory();
  }, []);

  const fetchMatchHistory = async () => {
    try {
      const res = await fetch(`${socketURL}/api/history/${user.id}`);
      const data = await res.json();
      setMatchHistory(data);
    } catch (err) {
      console.error('Failed to fetch match history:', err);
    }
  };

  const handleUpdateProfile = async () => {
    setIsLoading(true);
    try {
      const res = await fetch(`${socketURL}/api/profile/${user.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (!res.ok) throw new Error('Update failed');

      const updated = await res.json();
      await onUpdate(updated);
      setIsEditing(false);
    } catch (err) {
      alert('Failed to update profile');
    } finally {
      setIsLoading(false);
    }
  };

  const handleChangePassword = async () => {
    if (passwordForm.newPassword !== passwordForm.confirmPassword) {
      alert('Passwords do not match');
      return;
    }

    if (passwordForm.newPassword.length < 6) {
      alert('Password must be at least 6 characters');
      return;
    }

    setIsLoading(true);
    try {
      const res = await fetch(`${socketURL}/api/change-password/${user.id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          oldPassword: passwordForm.oldPassword,
          newPassword: passwordForm.newPassword
        })
      });

      if (!res.ok) throw new Error('Change password failed');

      alert('Password changed successfully');
      setPasswordForm({ oldPassword: '', newPassword: '', confirmPassword: '' });
      setShowPasswordModal(false);
    } catch (err) {
      alert('Failed to change password');
    } finally {
      setIsLoading(false);
    }
  };

  const getRankColor = (level: string) => {
    switch (level) {
      case 'Bronze': return 'from-amber-600 to-amber-400';
      case 'Silver': return 'from-gray-400 to-gray-200';
      case 'Gold': return 'from-yellow-500 to-yellow-300';
      case 'Crystal': return 'from-cyan-400 to-blue-300';
      default: return 'from-gray-400 to-gray-300';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      {/* Header */}
      <div className="bg-white shadow-lg">
        <div className="container mx-auto px-4 py-6 flex items-center justify-between">
          <button onClick={onBack} className="flex items-center gap-2 text-blue-600 hover:text-blue-800 font-semibold">
            <ArrowLeft size={20} /> Back
          </button>
          <h1 className="text-2xl font-black text-gray-800">My Profile</h1>
          <Button variant="ghost" size="sm" onClick={onLogout} className="text-red-600">
            Logout
          </Button>
        </div>
      </div>

      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Profile Card */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-3xl shadow-lg border border-gray-200 p-8 text-center sticky top-8">
              {/* Avatar */}
              {user.avatar_url ? (
                <img
                  src={user.avatar_url}
                  alt={user.display_name}
                  className="w-24 h-24 mx-auto mb-4 rounded-full object-cover shadow-lg border-4 border-white"
                  onError={(e) => {
                    // Fallback to initial if image fails
                    e.currentTarget.style.display = 'none';
                  }}
                />
              ) : (
                <div className={`w-24 h-24 mx-auto mb-4 rounded-full bg-gradient-to-br ${getRankColor(user.rank_level)} flex items-center justify-center text-4xl font-black text-white shadow-lg`}>
                  {user.display_name?.[0]?.toUpperCase() || 'U'}
                </div>
              )}

              <h2 className="text-2xl font-black text-gray-800 mb-1">{user.display_name}</h2>
              <p className="text-gray-500 text-sm mb-4">{user.full_name || 'No name set'}</p>

              {/* Rank Badge */}
              <div className={`bg-gradient-to-r ${getRankColor(user.rank_level)} text-white rounded-full px-6 py-2 font-bold text-center mb-4`}>
                {user.rank_level}
              </div>

              {/* Level Badge */}
              {user.user_level && (
                (() => {
                  const tierInfo = getTierInfo(user.user_level);
                  return (
                    <div
                      className="text-white rounded-full px-6 py-2 font-bold text-center mb-6"
                      style={{ backgroundColor: tierInfo?.color }}
                    >
                      {tierInfo?.name} • Lv {user.user_level}
                    </div>
                  );
                })()
              )}

              {/* Rank Score */}
              <div className="bg-gray-50 rounded-xl p-4 mb-6">
                <div className="text-gray-600 text-sm font-semibold">Rank Points</div>
                <div className="text-3xl font-black text-blue-600">{user.rank_score}</div>
              </div>

              {!isEditing && (
                <Button
                  onClick={() => setIsEditing(true)}
                  className="w-full mb-3"
                >
                  <Edit2 size={16} className="mr-2" /> Edit Info
                </Button>
              )}

              <Button
                variant="secondary"
                onClick={() => setShowPasswordModal(true)}
                className="w-full mb-3"
              >
                <Lock size={16} className="mr-2" /> Change Password
              </Button>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Personal Information Card */}
            {!isEditing && (
              <div className="bg-white rounded-3xl shadow-lg border border-gray-200 p-6">
                <h3 className="text-xl font-black mb-6 text-gray-800">Thông Tin Cá Nhân</h3>

                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-gray-50 rounded-xl p-4">
                    <p className="text-xs text-gray-500 font-semibold uppercase tracking-wider">Tên Đầy Đủ</p>
                    <p className="text-lg font-bold text-gray-800 mt-2">{user.full_name || '—'}</p>
                  </div>

                  <div className="bg-gray-50 rounded-xl p-4">
                    <p className="text-xs text-gray-500 font-semibold uppercase tracking-wider">Ngày Sinh</p>
                    <p className="text-lg font-bold text-gray-800 mt-2">
                      {user.date_of_birth ? new Date(user.date_of_birth).toLocaleDateString('vi-VN') : '—'}
                    </p>
                  </div>

                  <div className="bg-gray-50 rounded-xl p-4 col-span-2">
                    <p className="text-xs text-gray-500 font-semibold uppercase tracking-wider">Giới Thiệu</p>
                    <p className="text-base text-gray-700 mt-2 leading-relaxed">{user.bio || '—'}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Edit Profile Section */}
            {isEditing && (
              <div className="bg-white rounded-3xl shadow-lg border border-gray-200 p-8">
                <h3 className="text-2xl font-black mb-6 text-gray-800">Edit Personal Information</h3>

                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Full Name</label>
                    <input
                      type="text"
                      value={formData.full_name || ''}
                      onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-400 focus:outline-none"
                      placeholder="Enter full name"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Display Name</label>
                    <input
                      type="text"
                      value={formData.display_name || ''}
                      onChange={(e) => setFormData({ ...formData, display_name: e.target.value })}
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-400 focus:outline-none"
                      placeholder="Enter display name"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Date of Birth</label>
                    <input
                      type="date"
                      value={formData.date_of_birth || ''}
                      onChange={(e) => setFormData({ ...formData, date_of_birth: e.target.value })}
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-400 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Bio / About Me</label>
                    <textarea
                      value={formData.bio || ''}
                      onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-400 focus:outline-none h-24 resize-none"
                      placeholder="Tell us about yourself..."
                      maxLength={200}
                    />
                    <p className="text-xs text-gray-400 mt-1">{(formData.bio || '').length}/200</p>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Avatar URL</label>
                    <input
                      type="url"
                      value={formData.avatar_url || ''}
                      onChange={(e) => setFormData({ ...formData, avatar_url: e.target.value })}
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-400 focus:outline-none"
                      placeholder="https://example.com/avatar.jpg"
                    />
                    <p className="text-xs text-gray-400 mt-1">Paste a direct image URL</p>
                  </div>

                  <div className="flex gap-3 pt-4">
                    <Button
                      onClick={handleUpdateProfile}
                      loading={isLoading}
                      className="flex-1"
                    >
                      Save Changes
                    </Button>
                    <Button
                      variant="secondary"
                      onClick={() => {
                        setIsEditing(false);
                        setFormData({
                          full_name: user.full_name || '',
                          display_name: user.display_name || '',
                          date_of_birth: user.date_of_birth || '',
                          bio: user.bio || '',
                          avatar_url: user.avatar_url || ''
                        });
                      }}
                      className="flex-1"
                    >
                      Cancel
                    </Button>
                  </div>
                </div>
              </div>
            )}

            {/* Match History */}
            <div className="bg-white rounded-3xl shadow-lg border border-gray-200 p-8">
              <h3 className="text-2xl font-black mb-6 text-gray-800">Match History</h3>

              {matchHistory.length === 0 ? (
                <div className="text-center text-gray-500 py-8">
                  No matches played yet. Start playing to build your history!
                </div>
              ) : (
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {matchHistory.map((match) => (
                    <div key={match.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors">
                      <div className="flex-1">
                        <div className="font-semibold text-gray-800">
                          {match.game_type === 'tic-tac-toe' ? '🎮 Tic-Tac-Toe' : '● Caro'}
                          <span className="ml-3 text-sm text-gray-600">({match.mode})</span>
                        </div>
                        <div className="text-sm text-gray-600">
                          vs {match.opponent_name} • {new Date(match.played_at).toLocaleDateString()}
                        </div>
                      </div>

                      <div className={`font-bold text-lg px-4 py-2 rounded-lg ${match.result === 'win' ? 'bg-green-100 text-green-700' :
                        match.result === 'loss' ? 'bg-red-100 text-red-700' :
                          'bg-yellow-100 text-yellow-700'
                        }`}>
                        {match.result === 'win' ? '✓ Win' : match.result === 'loss' ? '✗ Loss' : '= Draw'}
                      </div>

                      {onReplayMatch && (
                        <button
                          onClick={() => onReplayMatch(match.id)}
                          className="ml-3 p-2 bg-blue-50 text-blue-600 rounded-full hover:bg-blue-100 transition"
                          title="Xem lại trận đấu"
                        >
                          <Eye size={18} />
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </main>

      {/* Change Password Modal */}
      {showPasswordModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-3xl shadow-lg border border-gray-200 p-8 max-w-md w-full">
            <h2 className="text-2xl font-black mb-6 text-gray-800">Change Password</h2>

            <div className="space-y-4 mb-6">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Current Password</label>
                <input
                  type="password"
                  value={passwordForm.oldPassword}
                  onChange={(e) => setPasswordForm({ ...passwordForm, oldPassword: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-400 focus:outline-none"
                  placeholder="Enter current password"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">New Password</label>
                <input
                  type="password"
                  value={passwordForm.newPassword}
                  onChange={(e) => setPasswordForm({ ...passwordForm, newPassword: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-400 focus:outline-none"
                  placeholder="Enter new password"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Confirm Password</label>
                <input
                  type="password"
                  value={passwordForm.confirmPassword}
                  onChange={(e) => setPasswordForm({ ...passwordForm, confirmPassword: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-400 focus:outline-none"
                  placeholder="Confirm new password"
                />
              </div>
            </div>

            <div className="flex gap-3">
              <Button
                onClick={handleChangePassword}
                loading={isLoading}
                className="flex-1"
              >
                Change Password
              </Button>
              <Button
                variant="secondary"
                onClick={() => {
                  setShowPasswordModal(false);
                  setPasswordForm({ oldPassword: '', newPassword: '', confirmPassword: '' });
                }}
                className="flex-1"
              >
                Cancel
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Profile;
