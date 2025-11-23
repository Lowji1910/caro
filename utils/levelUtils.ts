
/**
 * Calculate required XP for a specific level.
 * Matches logic in backend/database/schema.sql
 */
export const getRequiredXP = (level: number): number => {
    if (level <= 1) return 0;

    if (level <= 101) {
        return (level - 1) * 100;
    } else if (level <= 201) {
        return 10000 + (level - 101) * 200;
    } else if (level <= 301) {
        return 30000 + (level - 201) * 500;
    } else if (level <= 401) {
        return 80000 + (level - 301) * 1000;
    } else {
        return 180000 + (level - 401) * 2000;
    }
};

/**
 * Get progress for current level
 */
export const getLevelProgress = (xp: number, level: number) => {
    const currentLevelXP = getRequiredXP(level);
    const nextLevelXP = getRequiredXP(level + 1);

    const xpInLevel = Math.max(0, xp - currentLevelXP);
    const xpNeededForLevel = nextLevelXP - currentLevelXP;

    const percent = Math.min(100, Math.max(0, (xpInLevel / xpNeededForLevel) * 100));

    return {
        current: xpInLevel,
        max: xpNeededForLevel,
        percent,
        totalXP: xp
    };
};

/**
 * Get rank progress
 */
export const getRankProgress = (rankPoints: number) => {
    let rank = 'Bronze';
    let min = 0;
    let max = 500;
    let nextRank = 'Silver';

    if (rankPoints >= 2000) {
        rank = 'Crystal';
        min = 2000;
        max = 5000; // Arbitrary max for Crystal
        nextRank = 'Max Rank';
    } else if (rankPoints >= 1000) {
        rank = 'Gold';
        min = 1000;
        max = 2000;
        nextRank = 'Crystal';
    } else if (rankPoints >= 500) {
        rank = 'Silver';
        min = 500;
        max = 1000;
        nextRank = 'Gold';
    }

    const current = rankPoints - min;
    const total = max - min;
    const percent = Math.min(100, Math.max(0, (current / total) * 100));

    return {
        rank,
        nextRank,
        current,
        max: total,
        percent,
        totalPoints: rankPoints
    };
};
