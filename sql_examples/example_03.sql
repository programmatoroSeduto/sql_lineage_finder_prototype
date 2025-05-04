
SELECT DISTINCT  
col2, AVG(CASE WHEN col4 IS NOT NULL THEN value_vl ELSE 0.0 END) AS value_avg_vl
FROM (
    SELECT DISTINCT 
    col2, col4, CASE WHEN value_vl > 0 THEN value_vl / 2 else value_vl * 2 END AS value_vl
    FROM (
        SELECT 
        ROW_NUMBER() OVER (PARTITION BY col111, col222 ORDER BY col333),
        col1,col2, col3, col4, value_vl
        FROM crazy_table
    )
    WHERE 1=1
)
GROUP BY 1
HAVING ROUND(SUM(value_vl), 0) < 0
ORDER BY col2, -value_vl