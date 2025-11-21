-- Migration: Add game_levels and tiers tables for database-driven ranking system
-- Run this in phpMyAdmin SQL tab

USE tic_tac_toe_db;

-- Table 1: game_levels (Maps scores to levels 1-500)
CREATE TABLE IF NOT EXISTS game_levels (
    level INT PRIMARY KEY,
    required_score INT NOT NULL,
    INDEX idx_score (required_score)
);

-- Table 2: tiers (Maps level ranges to tier names and colors)
CREATE TABLE IF NOT EXISTS tiers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    color VARCHAR(20) NOT NULL,
    description TEXT,
    min_level INT NOT NULL,
    max_level INT NOT NULL,
    INDEX idx_level_range (min_level, max_level)
);

-- Populate game_levels (Sample: 100 points per level for first 100 levels, then scaled)
-- Level 1-100: 100 points each
INSERT INTO game_levels (level, required_score) VALUES (1, 0);
INSERT INTO game_levels (level, required_score)
SELECT 
    lvl,
    (lvl - 1) * 100
FROM (
    SELECT @row := @row + 1 as lvl
    FROM (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t1,
         (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t2,
         (SELECT @row := 1) r
    LIMIT 100
) levels
WHERE lvl > 1 AND lvl <= 100;

-- Level 101-200: 200 points each (starting from 10,000)
INSERT INTO game_levels (level, required_score)
SELECT 
    lvl + 100,
    10000 + (lvl * 200)
FROM (
    SELECT @row2 := @row2 + 1 as lvl
    FROM (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t1,
         (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t2,
         (SELECT @row2 := 0) r
    LIMIT 100
) levels;

-- Level 201-300: 500 points each (starting from 30,000)
INSERT INTO game_levels (level, required_score)
SELECT 
    lvl + 200,
    30000 + (lvl * 500)
FROM (
    SELECT @row3 := @row3 + 1 as lvl
    FROM (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t1,
         (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t2,
         (SELECT @row3 := 0) r
    LIMIT 100
) levels;

-- Level 301-400: 1000 points each (starting from 80,000)
INSERT INTO game_levels (level, required_score)
SELECT 
    lvl + 300,
    80000 + (lvl * 1000)
FROM (
    SELECT @row4 := @row4 + 1 as lvl
    FROM (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t1,
         (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t2,
         (SELECT @row4 := 0) r
    LIMIT 100
) levels;

-- Level 401-500: 2000 points each (starting from 180,000)
INSERT INTO game_levels (level, required_score)
SELECT 
    lvl + 400,
    180000 + (lvl * 2000)
FROM (
    SELECT @row5 := @row5 + 1 as lvl
    FROM (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t1,
         (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t2,
         (SELECT @row5 := 0) r
    LIMIT 100
) levels;

-- Populate tiers (Example tier structure)
INSERT INTO tiers (name, color, description, min_level, max_level) VALUES
    ('Tân Thủ', '#9E9E9E', 'Người mới bắt đầu', 1, 10),
    ('Đồng Học', '#CD7F32', 'Bậc đồng học', 11, 30),
    ('Bạc Học', '#C0C0C0', 'Bậc bạc học', 31, 50),
    ('Nhập Môn', '#4CAF50', 'Đã nhập môn', 51, 100),
    ('Tinh Thông', '#2196F3', 'Tinh thông võ nghệ', 101, 150),
    ('Đại Sư', '#9C27B0', 'Đại sư võ lâm', 151, 200),
    ('Tôn Giả', '#FF9800', 'Tôn giả cao cường', 201, 300),
    ('Chí Tôn', '#F44336', 'Chí tôn thiên hạ', 301, 400),
    ('Huyền Thánh', '#FFD700', 'Huyền thánh vô song', 401, 500);
