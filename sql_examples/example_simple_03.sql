SELECT
COALESCE(col_a, '') AS col_a_new,
col_c,
ROUND(SUM(col_b),2) AS sum_col_b
FROM tab1 tab 
GROUP BY col_c, col_a
HAVING SUM(col_b) > 3/4 AND AVG(col_b) < 3
ORDER BY 2,1