export interface TierInfo {
  name: string;
  color: string;
  description: string;
}

export const getTierInfo = (level?: number): TierInfo | null => {
  if (!level) return null;
  
  const tier = Math.floor((level - 1) / 50) + 1;
  
  const tiers: TierInfo[] = [
    { name: 'Tân Thủ', color: '#9E9E9E', description: 'Người mới' },
    { name: 'Nhập Môn', color: '#4CAF50', description: 'Mới vào nghề' },
    { name: 'Xuất Sắc', color: '#2196F3', description: 'Bắt đầu giỏi' },
    { name: 'Tinh Anh', color: '#9C27B0', description: 'Thành phần ưu tú' },
    { name: 'Cao Thủ', color: '#F44336', description: 'Người chơi giỏi' },
    { name: 'Danh Thủ', color: '#FF9800', description: 'Người nổi tiếng giỏi' },
    { name: 'Đại Sư', color: '#FFD700', description: 'Bậc thầy' },
    { name: 'Tông Sư', color: '#E91E63', description: 'Bậc thầy của các bậc thầy' },
    { name: 'Huyền Thoại', color: '#00BCD4', description: 'Legend' },
    { name: 'Chí Tôn', color: '#000000', description: 'Tối cao, vô địch' }
  ];
  
  return tiers[tier - 1] || tiers[9];
};

export const getTierColor = (level?: number): string => {
  const tierInfo = getTierInfo(level);
  return tierInfo?.color || '#9E9E9E';
};

export const getTierName = (level?: number): string => {
  const tierInfo = getTierInfo(level);
  return tierInfo?.name || 'Chí Tôn';
};
