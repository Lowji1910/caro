CREATE DATABASE IF NOT EXISTS tic_tac_toe_db;
USE tic_tac_toe_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    display_name VARCHAR(50),
    full_name VARCHAR(100),
    date_of_birth DATE,
    bio TEXT,
    avatar_url VARCHAR(255),
    rank_score INT DEFAULT 0,
    rank_level VARCHAR(20) DEFAULT 'Bronze',
    user_level INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS match_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player1_id INT,
    player2_id INT,
    winner_id INT,
    game_type VARCHAR(20),
    mode VARCHAR(20),
    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player1_id) REFERENCES users(id),
    FOREIGN KEY (player2_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS user_levels_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    level INT NOT NULL,
    rank_score INT NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Insert dữ liệu mẫu
INSERT INTO users (username, password, display_name, full_name, rank_score, rank_level, user_level) 
VALUES ('player1', 'password', 'Player One', 'Player One', 1200, 'Gold', 75) 
ON DUPLICATE KEY UPDATE username=username;