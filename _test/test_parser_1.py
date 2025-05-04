
import sqlparse

sql = """\
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
"""

pql = sqlparse.parse(sql)

print(pql)
'''
(<Statement ' WITH ...' at 0x21D227AB120>,)
'''

pql_stat = [x for x in pql[0].tokens if not x.is_whitespace]

for idx, item in enumerate(pql_stat):
    print(f"[{idx}] =====")
    print(pql_stat[idx])

'''
[0] =====
WITH
[1] =====
tab AS (
[2] =====
SELECT
[3] =====
t2.col3 AS dim,
ROW_NUMBER() OVER (PARTITION BY col2 ORDER BY col1, col2) AS rowno,
NVL(col1, col2, col3) + NVL(col3, 3.14) AS raw_kpi
[4] =====
FROM
[5] =====
sch_raw_funny_it.tab1 AS fn
[6] =====
LEFT JOIN
[7] =====
sch_raw_another_fun.tab2 AS t2
[8] =====
ON
[9] =====
(
[10] =====
fn.col_join = CONCAT(t2.col_join, '#', t2.col1 AND fn.col5 IS NOT NULL)
[11] =====
LEFT JOIN
[12] =====
sch_raw_another_fun.tab2 AS t3
[13] =====
ON
[14] =====
( fn.col_join = CONCAT(t2.col_join, '#', t2.col1 AND fn.col5 IS NOT NULL)

WHERE t2.col6_archi IS NULL
)
[15] =====
,
[16] =====
tab_pre_final AS (
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
[17] =====
SELECT
[18] =====
dim,
SUM(kpi_converted) AS kpi_final
[19] =====
FROM
[20] =====
tab_pre_final
[21] =====
WHERE dim <> '' AND dim IS NOT NULL
AND dim IN (SELECT DISTINCT dim_raw FROM sch_raw_another_fun.tab2) AND dim <> 'NON USARE'

[22] =====
GROUP BY
[23] =====
dim, dim
[24] =====
HAVING
[25] =====
SUM(kpi_converted)
[26] =====
BETWEEN
[27] =====
50
[28] =====
AND
[29] =====
5000
[30] =====
ORDER BY
[31] =====
NVL(kpi_final, 0.7), dim, dim
[32] =====
LIMIT
[33] =====
1
'''

print(pql_stat)
'''
[<CTE 'WITH' at 0x195AD5B38E0>, # 0
<Identifier 'tab AS...' at 0x195AD5CC900>, 
<DML 'SELECT' at 0x195AD5B3CA0>, 
<IdentifierList 't2.col...' at 0x195AD5D15F0>, 
<Keyword 'FROM' at 0x195AD5BF520>, 
<Identifier 'sch_ra...' at 0x195AD5CC350>, # 5
<Keyword 'LEFT J...' at 0x195AD5BF8E0>, 
<Identifier 'sch_ra...' at 0x195AD5CC3C0>, 
<Keyword 'ON' at 0x195AD5BFCA0>, 
<Punctuation '(' at 0x195AD5BFD60>, 
<Comparison 'fn.col...' at 0x195AD5D1120>, # 10
<Keyword 'LEFT J...' at 0x195AD5C0A00>, 
<Identifier 'sch_ra...' at 0x195AD5CC5F0>, 
<Keyword 'ON' at 0x195AD5C0DC0>, 
<Parenthesis '( fn.c...' at 0x195AD5B66D0>, 
<Punctuation ',' at 0x195AD5C30A0>, # 15
<Identifier 'tab_pr...' at 0x195AD5CEBA0>, 
<DML 'SELECT' at 0x195AD5C6520>, 
<IdentifierList 'dim, ...' at 0x195AD5D1970>, 
<Keyword 'FROM' at 0x195AD5C6B20>, 
<Identifier 'tab_pr...' at 0x195AD5CECF0>, # 20 
<Where 'WHERE ...' at 0x195AD5CC190>, 
<Keyword 'GROUP ...' at 0x195AD5C7E20>, 
<IdentifierList 'dim, d...' at 0x195AD5D1900>, 
<Keyword 'HAVING' at 0x195AD5C9100>, 
<Function 'SUM(kp...' at 0x195AD5CC0B0>, # 25
<Keyword 'BETWEEN' at 0x195AD5C93A0>, 
<Integer '50' at 0x195AD5C9460>, 
<Keyword 'AND' at 0x195AD5C9520>, 
<Integer '5000' at 0x195AD5C95E0>, 
<Keyword 'ORDER ...' at 0x195AD5C96A0>, 
<IdentifierList 'NVL(kp...' at 0x195AD5D1AC0>, 
<Keyword 'LIMIT' at 0x195AD5C9CA0>, 
<Integer '1' at 0x195AD5C9D60>]
'''

print(pql_stat[14])
'''
( fn.col_join = CONCAT(t2.col_join, '#', t2.col1 AND fn.col5 IS NOT NULL)

WHERE t2.col6_archi IS NULL
)
'''

print(type(pql_stat[14]))
'''
<class 'sqlparse.sql.Parenthesis'>
'''

print(pql_stat[14].tokens)
'''
[<Punctuation '(' at 0x1FF5839DDC0>, 
<Whitespace ' ' at 0x1FF5839DE20>, 
<Comparison 'fn.col...' at 0x1FF583A93C0>, 
<Newline ' ' at 0x1FF5839FA00>, 
<Newline ' ' at 0x1FF5839FA60>, 
<Where 'WHERE ...' at 0x1FF58399A50>, 
<Punctuation ')' at 0x1FF5839FE80>]
'''

print(pql_stat[21].tokens)
'''
[<Keyword 'WHERE' at 0x1DF80946820>, 
<Whitespace ' ' at 0x1DF80946880>, 
<Comparison 'dim <>...' at 0x1DF8094DF20>, 
<Whitespace ' ' at 0x1DF80946AC0>, 
<Keyword 'AND' at 0x1DF80946B20>, 
<Whitespace ' ' at 0x1DF80946B80>, 
<Identifier 'dim' at 0x1DF8094D3C0>, 
<Whitespace ' ' at 0x1DF80946C40>, 
<Keyword 'IS' at 0x1DF80946CA0>, 
<Whitespace ' ' at 0x1DF80946D00>, 
<Keyword 'NOT NU...' at 0x1DF80946D60>, 
<Whitespace ' ' at 0x1DF80946DC0>, 
<Newline ' ' at 0x1DF80946E20>, 
<Keyword 'AND' at 0x1DF80946E80>, 
<Whitespace ' ' at 0x1DF80946EE0>, 
<Identifier 'dim' at 0x1DF8094D4A0>, 
<Whitespace ' ' at 0x1DF80946FA0>, 
<Keyword 'IN' at 0x1DF80947040>, 
<Whitespace ' ' at 0x1DF809470A0>, 
<Parenthesis '(SELEC...' at 0x1DF80936740>, 
<Whitespace ' ' at 0x1DF809475E0>, 
<Keyword 'AND' at 0x1DF80947640>, 
<Whitespace ' ' at 0x1DF809476A0>, 
<Comparison 'dim <>...' at 0x1DF8094DF90>, 
<Newline ' ' at 0x1DF809478E0>]
'''

print(''.join([str(x) for x in pql_stat[21].tokens]))
'''
WHERE dim <> '' AND dim IS NOT NULL
AND dim IN (SELECT DISTINCT dim_raw FROM sch_raw_another_fun.tab2) AND dim <> 'NON USARE'
'''

print(pql_stat[16].tokens)
'''
[<Name 'tab_pr...' at 0x29B7A653100>, 
<Whitespace ' ' at 0x29B7A653160>, 
<Keyword 'AS' at 0x29B7A6531C0>, 
<Whitespace ' ' at 0x29B7A653220>, 
<Parenthesis '( SELE...' at 0x29B7A64D7B0>]
'''

print(pql_stat[16].tokens[4].tokens)
'''
[<Punctuation '(' at 0x24AF4BF3280>, # 0
<Newline ' ' at 0x24AF4BF32E0>, 
<DML 'SELECT' at 0x24AF4BF3340>, 
<Whitespace ' ' at 0x24AF4BF33A0>, 
<Newline ' ' at 0x24AF4BF3400>, 
<IdentifierList 'dim, M...' at 0x24AF4C017B0>, # 5 
<Punctuation ',' at 0x24AF4BF51C0>, 
<Newline ' ' at 0x24AF4BF5220>, 
<Comment '-- ROU...' at 0x24AF4BEC200>, 
<Keyword 'FROM' at 0x24AF4BF5340>, 
<Whitespace ' ' at 0x24AF4BF53A0>, # 10
<Identifier '(SELEC...' at 0x24AF4C01580>, 
<Whitespace ' ' at 0x24AF4BF58E0>, 
<Newline ' ' at 0x24AF4BF5940>, 
<Where 'WHERE ...' at 0x24AF4BFC190>, 
<Keyword 'LIMIT' at 0x24AF4BF6220>, # 15
<Whitespace ' ' at 0x24AF4BF6280>, 
<Integer '100' at 0x24AF4BF62E0>, 
<Whitespace ' ' at 0x24AF4BF6340>, 
<Newline ' ' at 0x24AF4BF63A0>, 
<Punctuation ')' at 0x24AF4BF6400>] # 20
'''

print(pql_stat[16].tokens[4].tokens[11])
'''
(SELECT DISTINCT * FROM tab) tab
'''

print(pql_stat[16].tokens[4].tokens[11].tokens)
'''
[<Parenthesis '(SELEC...' at 0x28DCECFD740>, <Whitespace ' ' at 0x28DCED04880>, <Identifier 'tab' at 0x28DCED0F2E0>]
'''