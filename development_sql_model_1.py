
from sql_parse_query_algorithm import *

sql = """
SELECT 
a, 
b, 
c
FROM tab tab
FULL OUTER JOIN tub ON (tab.key = tub.key)
WHERE 1=1 OR 1 BETWEEN 1 AND 1
GROUP BY AAAA
HAVING AAAA > 7
ORDER BY 3,2,b
LIMIT 100
"""

pql = sqlparse.parse(sql)
print(type(pql))
'''
<class 'tuple'>
'''
print(pql[0].tokens)
'''
[<Newline ' ' at 0x2990AD7E220>, <DML 'SELECT' at 0x2990AD7E1C0>, <Whitespace ' ' at 0x2990AD7E3A0>, <Newline ' ' at 0x2990AD7E6A0>, <IdentifierList 'a, b,...' at 0x2990AD7C890>, <Newline ' ' at 0x2990AD7EA60>, <Keyword 'FROM' at 0x2990AD7EAC0>, <Whitespace ' ' at 0x2990AD7EB20>, <Identifier 'tab tab' at 0x2990AD7CC10>, <Newline ' ' at 0x2990AD7ECA0>, <Keyword 'LEFT J...' at 0x2990AD7ED00>, <Whitespace ' ' at 0x2990AD7ED60>, <Identifier 'tub' at 0x2990AD7CCF0>, <Whitespace ' ' at 0x2990AD7EE20>, <Keyword 'ON' at 0x2990AD7EE80>, <Whitespace ' ' at 0x2990AD7EEE0>, <Parenthesis '(tab.k...' at 0x2990AD7C900>, <Newline ' ' at 0x2990AD8F3A0>, <Where 'WHERE ...' at 0x2990AD7C970>, <Keyword 'GROUP ...' at 0x2990AD8FAC0>, <Whitespace ' ' at 0x2990AD8FB20>, <Identifier 'AAAA' at 0x2990AD7CD60>, <Newline ' ' at 0x2990AD8FBE0>, <Keyword 'HAVING' at 0x2990AD8FC40>, <Whitespace ' ' at 0x2990AD8FCA0>, <Comparison 'AAAA >...' at 0x2990AD7CF90>, <Newline ' ' at 0x2990AD8FEE0>, <Keyword 'ORDER ...' at 0x2990AD8FF40>, <Whitespace ' ' at 0x2990AD8FFA0>, <IdentifierList '3,2,b' at 0x2990AD96040>, <Newline ' ' at 0x2990AD90220>, <Keyword 'LIMIT' at 0x2990AD90280>, <Whitespace ' ' at 0x2990AD902E0>, <Integer '100' at 0x2990AD90340>, <Newline ' ' at 0x2990AD903A0>]
'''
print([str(type(x)) for x in pql[0].tokens])
'''
["<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.IdentifierList'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Identifier'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Identifier'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Parenthesis'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Where'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Identifier'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Comparison'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.IdentifierList'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>"]
'''


sql = "FROM tab1"
pql = sqlparse.parse(sql)
print("=====")
print(sql)
print(pql[0].tokens)
'''
[<Keyword 'FROM' at 0x2934BA72460>, <Whitespace ' ' at 0x2934BA724C0>, <Identifier 'tab1' at 0x2934BA79120>]
'''


sql = "FROM tab1 AS table"
pql = sqlparse.parse(sql)
print("=====")
print(sql)
print(pql[0].tokens)
'''
[<Keyword 'FROM' at 0x2934BA72460>, <Whitespace ' ' at 0x2934BA724C0>, <Identifier 'tab1' at 0x2934BA79120>]
'''


sql = "FROM tab1 AS table LEFT JOIN tab2 AS another_table ON ( table.key = another_table.key )"
pql = sqlparse.parse(sql)
print("=====")
print(sql)
print(pql[0].tokens)
'''
[<Keyword 'FROM' at 0x203569738E0>, <Whitespace ' ' at 0x20356973940>, <Identifier 'tab1 A...' at 0x2035697A430>, <Whitespace ' ' at 0x20356973B80>, <Keyword 'LEFT J...' at 0x20356973BE0>, <Whitespace ' ' at 0x20356973C40>, <Identifier 'tab2 A...' at 0x2035697A4A0>, <Whitespace ' ' at 0x20356973E80>, <Keyword 'ON' at 0x20356973EE0>, <Whitespace ' ' at 0x20356973F40>, <Parenthesis '( tabl...' at 0x2035697A200>]
'''



sql = "FROM (select distinct key from tab1) AS table LEFT JOIN tab2 AS another_table ON ( table.key = another_table.key )"
pql = sqlparse.parse(sql)
print("=====")
print(sql)
print(pql[0].tokens)
'''
[<Keyword 'FROM' at 0x26C5DA2C580>, <Whitespace ' ' at 0x26C5DA2C520>, <Identifier '(selec...' at 0x26C5DA2B6D0>, <Whitespace ' ' at 0x26C5DA2CB80>, <Keyword 'LEFT J...' at 0x26C5DA2CBE0>, <Whitespace ' ' at 0x26C5DA2CC40>, <Identifier 'tab2 A...' at 0x26C5DA2B890>, <Whitespace ' ' at 0x26C5DA2CE80>, <Keyword 'ON' at 0x26C5DA2CEE0>, <Whitespace ' ' at 0x26C5DA2CF40>, <Parenthesis '( tabl...' at 0x26C5DA2B660>]
'''