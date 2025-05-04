WITH 

tab AS (
SELECT 
t2.col3 AS dim, 
ROW_NUMBER() OVER (PARTITION BY col2 ORDER BY col1, col2) AS rowno,
NVL(col1, col2, col3) + NVL(col3, 3.14) AS raw_kpi
FROM sch_raw_funny_it.tab1 AS fn
LEFT JOIN sch_raw_another_fun.tab2 AS t2
ON ( fn.col_join = CONCAT(t2.col_join, '#', t2.col1 AND fn.col5 IS NOT NULL)
LEFT JOIN sch_raw_another_fun.tab2 AS t3
ON ( fn.col_join = CONCAT(t2.col_join, '#', t2.col1 AND fn.col5 IS NOT NULL)

WHERE t2.col6_archi IS NULL
)

,tab_pre_final AS (
SELECT 
dim,
MIN(rowno) + rowno AS idx,
raw_kpi AS kpi_basic,
raw_kpi * 3.14/2.71 AS kpi_converted,
-- ROUND(3.14/2.71, 2) AS conversion_factor
FROM (SELECT DISTINCT * FROM tab) tab 
WHERE 1=1
    AND rowno BETWEEN 26 AND 567
LIMIT 100 
)

SELECT 
dim, 
SUM(kpi_converted) AS kpi_final
FROM tab_pre_final

WHERE dim <> '' AND dim IS NOT NULL 
AND dim IN (SELECT DISTINCT dim_raw FROM sch_raw_another_fun.tab2) AND dim <> 'NON USARE'
GROUP BY dim, dim
HAVING SUM(kpi_converted) BETWEEN 50 AND 5000
ORDER BY NVL(kpi_final, 0.7), dim, dim
LIMIT 1