-- Check if moves column exists and its data type
SELECT 
    COLUMN_NAME, 
    DATA_TYPE, 
    COLUMN_TYPE,
    IS_NULLABLE
FROM 
    INFORMATION_SCHEMA.COLUMNS
WHERE 
    TABLE_SCHEMA = 'tic_tac_toe_db' 
    AND TABLE_NAME = 'match_history'
    AND COLUMN_NAME = 'moves';
