
WITH 

tab1 AS (
SELECT 
col1, 
CASE 
    WHEN col2 IS NULL THEN col1 
    WHEN col2 LIKE '%NON USARE%'
END AS col2, 
coalesce(col3::decimal(15,0)::string, '') AS col3 
FROM tab1
)

,

tab2 AS (
SELECT
'tab2' AS source_ds, 
*
FROM tab1
WHERE 1=1 AND 2=2
)

,pre_final AS (
SELECT 
'source_1'
col1, 
COALESCE(col2, col3, 'NON ESISTE') AS col2
col3 
FROM tab1
WHERE 1=1
AND col1 IS NOT NULL 
AND (col3 <> 0.0 OR col2 == 'ciao')

UNION ALL 

SELECT 
source_ds, col1, col2, col3
FROM 
)

,final AS (
SELECT 
*
FROM pre_final
)

SELECT DISTINCT col1, col3 FROM final ORDER BY col3 LIMIT 50