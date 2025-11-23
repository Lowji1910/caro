-- =============================================
-- Caro & Tic-Tac-Toe Game Database Schema
-- CLEAN NORMALIZED VERSION
-- =============================================

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `tic_tac_toe_db`;
USE `tic_tac_toe_db`;

-- =============================================
-- TABLE 1: ranks (Bronze, Silver, Gold, Crystal)
-- Based on rank_score
-- =============================================
CREATE TABLE `ranks` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(20) NOT NULL UNIQUE,
  `min_score` INT NOT NULL,
  `max_score` INT NULL,
  `color` VARCHAR(20) NOT NULL,
  `description` VARCHAR(255),
  INDEX `idx_score_range` (`min_score`, `max_score`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Insert 4 ranks
INSERT INTO `ranks` (`id`, `name`, `min_score`, `max_score`, `color`, `description`) VALUES
(1, 'Bronze', 0, 499, '#CD7F32', 'Mức người mới - Vừa bắt đầu chơi'),
(2, 'Silver', 500, 999, '#C0C0C0', 'Mức trung bình - Đang phát triển kỹ năng'),
(3, 'Gold', 1000, 1999, '#FFD700', 'Mức nâng cao - Người chơi mạnh'),
(4, 'Crystal', 2000, NULL, '#00BCD4', 'Mức cao nhất - Người chơi chuyên nghiệp');

-- =============================================
-- TABLE 2: game_levels (Levels 1-500)
-- Based on XP/score progression
-- =============================================
CREATE TABLE `game_levels` (
  `level` INT PRIMARY KEY,
  `required_score` INT NOT NULL,
  INDEX `idx_required_score` (`required_score`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Insert level progression (simplified - 100 points per level for first 100)
-- Level 1-100: 100 points each
INSERT INTO `game_levels` (`level`, `required_score`) VALUES (1, 0);
INSERT INTO `game_levels` (`level`, `required_score`)
SELECT 
    @row := @row + 1,
    (@row - 1) * 100
FROM 
    (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
     UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t1,
    (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
     UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t2,
    (SELECT @row := 1) r
LIMIT 99;

-- Level 101-200: 200 points each (starting from 10,000)
INSERT INTO `game_levels` (`level`, `required_score`)
SELECT 
    100 + @row2 := @row2 + 1,
    10000 + (@row2 * 200)
FROM 
    (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
     UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t1,
    (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
     UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t2,
    (SELECT @row2 := 0) r
LIMIT 100;

-- Level 201-300: 500 points each (starting from 30,000)
INSERT INTO `game_levels` (`level`, `required_score`)
SELECT 
    200 + @row3 := @row3 + 1,
    30000 + (@row3 * 500)
FROM 
    (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
     UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t1,
    (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
     UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t2,
    (SELECT @row3 := 0) r
LIMIT 100;

-- Level 301-400: 1000 points each (starting from 80,000)
INSERT INTO `game_levels` (`level`, `required_score`)
SELECT 
    300 + @row4 := @row4 + 1,
    80000 + (@row4 * 1000)
FROM 
    (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
     UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t1,
    (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
     UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t2,
    (SELECT @row4 := 0) r
LIMIT 100;

-- Level 401-500: 2000 points each (starting from 180,000)
INSERT INTO `game_levels` (`level`, `required_score`)
SELECT 
    400 + @row5 := @row5 + 1,
    180000 + (@row5 * 2000)
FROM 
    (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
     UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t1,
    (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
     UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t2,
    (SELECT @row5 := 0) r
LIMIT 100;

-- =============================================
-- TABLE 3: tiers (10 tier titles/danh hiệu)
-- Based on user_level (50 levels per tier)
-- =============================================
CREATE TABLE `tiers` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(50) NOT NULL,
  `color` VARCHAR(20) NOT NULL,
  `description` VARCHAR(255),
  `min_level` INT NOT NULL,
  `max_level` INT NOT NULL,
  INDEX `idx_level_range` (`min_level`, `max_level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Insert 10 tiers (50 levels each) matching frontend
INSERT INTO `tiers` (`id`, `name`, `color`, `description`, `min_level`, `max_level`) VALUES
(1, 'Tân Thủ', '#9E9E9E', 'Người mới', 1, 50),
(2, 'Nhập Môn', '#4CAF50', 'Mới vào nghề', 51, 100),
(3, 'Xuất Sắc', '#2196F3', 'Bắt đầu giỏi', 101, 150),
(4, 'Tinh Anh', '#9C27B0', 'Thành phần ưu tú', 151, 200),
(5, 'Cao Thủ', '#F44336', 'Người chơi giỏi', 201, 250),
(6, 'Danh Thủ', '#FF9800', 'Người nổi tiếng giỏi', 251, 300),
(7, 'Đại Sư', '#FFD700', 'Bậc thầy', 301, 350),
(8, 'Tông Sư', '#E91E63', 'Bậc thầy của các bậc thầy', 351, 400),
(9, 'Huyền Thoại', '#00BCD4', 'Legend', 401, 450),
(10, 'Chí Tôn', '#000000', 'Tối cao, vô địch', 451, 500);

-- =============================================
-- TABLE 4: users (WITH FOREIGN KEYS)
-- =============================================
CREATE TABLE `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(50) NOT NULL UNIQUE,
  `password` VARCHAR(255) NOT NULL,
  `display_name` VARCHAR(100) NOT NULL,
  `full_name` VARCHAR(100),
  `email` VARCHAR(100) UNIQUE,
  `date_of_birth` DATE,
  `bio` TEXT,
  `avatar_url` VARCHAR(255),
  
  -- XP System (Leveling - Always increases)
  `xp` INT NOT NULL DEFAULT 0,
  `level` INT NOT NULL DEFAULT 1,
  
  -- Rank System (Competitive - Can go down)
  `rank_points` INT NOT NULL DEFAULT 0,
  `rank_id` INT NOT NULL DEFAULT 1,
  
  -- Timestamps
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  -- Foreign Keys
  FOREIGN KEY (`rank_id`) REFERENCES `ranks`(`id`),
  FOREIGN KEY (`level`) REFERENCES `game_levels`(`level`),
  
  -- Indexes
  INDEX `idx_xp` (`xp`),
  INDEX `idx_level` (`level`),
  INDEX `idx_rank_points` (`rank_points`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- =============================================
-- TABLE 5: match_history
-- =============================================
CREATE TABLE `match_history` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `game_type` ENUM('tic-tac-toe', 'caro') NOT NULL,
  `mode` ENUM('practice', 'ranked') NOT NULL,
  `player1_id` INT NOT NULL,
  `player2_id` INT,
  `winner_id` INT,
  `result` ENUM('win', 'loss', 'draw') NOT NULL,
  `moves` JSON,
  `played_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (`player1_id`) REFERENCES `users`(`id`),
  FOREIGN KEY (`player2_id`) REFERENCES `users`(`id`),
  FOREIGN KEY (`winner_id`) REFERENCES `users`(`id`),
  
  INDEX `idx_player1` (`player1_id`),
  INDEX `idx_player2` (`player2_id`),
  INDEX `idx_played_at` (`played_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- =============================================
-- TABLE 6: user_levels_history
-- =============================================
CREATE TABLE `user_levels_history` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  `level` INT NOT NULL,
  `xp` INT NOT NULL,
  `achieved_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
  
  INDEX `idx_user_level_history` (`user_id`, `achieved_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- =============================================
-- SAMPLE DATA: Create test users
-- =============================================
INSERT INTO `users` (`username`, `password`, `display_name`, `email`, `xp`, `level`, `rank_points`, `rank_id`) VALUES
('player1', 'scrypt:32768:8:1$fakehashedpassword1', 'Player 1', 'player1@example.com', 0, 1, 0, 1),
('player2', 'scrypt:32768:8:1$fakehashedpassword2', 'Player 2', 'player2@example.com', 0, 1, 0, 1);

COMMIT;

-- =============================================
-- Summary
-- =============================================
-- Tables created:
-- 1. ranks         - 4 ranks (Bronze, Silver, Gold, Crystal)
-- 2. game_levels   - 500 levels with score requirements
-- 3. tiers         - 10 tiers (Tân Thủ -> Chí Tôn)
-- 4. users         - User table with FKs to ranks & game_levels
-- 5. match_history - Game records
-- 6. user_levels_history - Level-up tracking

-- Key improvements:
-- ✅ Normalized schema (3NF)
-- ✅ Foreign Key constraints
-- ✅ Indexed for performance
-- ✅ rank_id FK instead of varchar rank_level
-- ✅ Clean, maintainable design
