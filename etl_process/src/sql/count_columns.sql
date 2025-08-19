SELECT 
    COUNT(*) as columns
FROM 
    information_schema.columns
WHERE
    table_schema = 'de_2506_a' AND
    table_name = 'sam_capstone'