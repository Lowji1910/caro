-- Add moves column to match_history table
-- This column will store the move history for match replays
ALTER TABLE match_history 
ADD COLUMN moves JSON DEFAULT NULL;
