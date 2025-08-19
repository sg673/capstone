SELECT 
    COUNT(*) as result
FROM 
    information_schema.columns
WHERE
    table_schema = 'de_2506_a' AND
    table_name = 'sam_capstone'