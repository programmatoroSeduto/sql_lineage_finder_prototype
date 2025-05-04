
import sqlparse
from sql_parse_query_algorithm import explore_sql_statement, explore_from_clause_part

sql = """
SELECT 
a, 
b, 
c
FROM tab AS tab
FULL OUTER JOIN (SELECT DISTINCT key FROM sch.tab) AS tub ON (tab.key = tub.key)
JOIN (SELECT DISTINCT key FROM sch.tab) tub ON (tab.key = tub.key)
FULL OUTER JOIN sch.tab AS tub ON (tab.key = tub.key)
LEFT JOIN sch.tab tub ON (tab.key = tub.key)
-- JOIN sch.tab tub USING (key)
RIGHT JOIN sch.tab as tub ON (tab.key = tub.key)
WHERE 1=1 OR 1 BETWEEN 1 AND 1
GROUP BY AAAA
HAVING AAAA > 7
ORDER BY 3,2,b
LIMIT 100
"""

pql = sqlparse.parse(sql)
pql_stat = pql[0].tokens
clause_select, clause_from, clause_where, clause_groupby, clause_having, clause_orderby, clause_limit = explore_sql_statement(pql_stat)

for part in clause_from:
    print(part)
    print(explore_from_clause_part(part))
    print("\n")

# print([str(type(x)) for x in from_clause_parts[1]])
# <JOIN stat> <qualcosa> <ON> <qualcosa>
# ["<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Identifier'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Parenthesis'>"]
