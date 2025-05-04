SELECT 
nvl(tab.a, tab.c) column_a, 
tab.b AS column_b
,tab.c
FROM tab1 AS tab
ORDER BY 2,1,3
;