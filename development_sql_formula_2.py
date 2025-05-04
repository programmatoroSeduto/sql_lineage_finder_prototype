
import sqlparse
from sql_parse_formula_algorithm import explore_select_formula

def test_sql(sql):
    pql = sqlparse.parse(sql)
    print("=====")
    print(pql[0].tokens)
    pql_stat = pql[0].tokens[0]
    print(pql_stat)
    explore_select_formula(pql_stat)
    print("\n\n")


# sql = "col1"
'''
[WRAPPER] formula_alias is: col1
[WRAPPER] formula_text is: col1
[WRAPPER] formula_sources is: ['???.col1']
'''

# sql = "tab1.col1"
'''
[WRAPPER] formula_alias is: col1
[WRAPPER] formula_text is: tab1.col1
[WRAPPER] formula_sources is: ['tab1.col1']
'''

# sql = "col1 AS column_alias"
'''
[WRAPPER] formula_alias is: column_alias
[WRAPPER] formula_text is: col1
[WRAPPER] formula_sources is: ['???.col1']
'''

# sql = "tab.b AS column_b"
'''
[WRAPPER] formula_alias is: column_b
[WRAPPER] formula_text is: tab.b
[WRAPPER] formula_sources is: ['tab.b']
'''

# sql = "tab.a + b AS value_vl"
'''
[WRAPPER] formula_alias is: value_vl
[WRAPPER] formula_text is: tab.a + b
[WRAPPER] formula_sources is: ['tab.a', '???.b']
'''

# sql = "tab.a + b + (tab2.c/d) AS col_vl"
'''
[WRAPPER] formula_alias is: col_vl
[WRAPPER] formula_text is: tab.a + b + (tab2.c/d)
[WRAPPER] formula_sources is: ['tab.a', '???.b', 'tab2.c', '???.d']
'''

# sql = "SUM(a)"
'''
[WRAPPER] formula_alias is: a
[WRAPPER] formula_text is: SUM(a)
[WRAPPER] formula_sources is: ['???.a']
'''

# sql = "SUM(a) sum_OF_a"
'''
[WRAPPER] formula_alias is: sum_OF_a
[WRAPPER] formula_text is: SUM(a)
[WRAPPER] formula_sources is: ['???.a']
'''

# sql = "SUM(a + b - tab.c) AS column_vl"
'''
[WRAPPER] formula_alias is: column_vl
[WRAPPER] formula_text is: SUM(a + b - tab.c)
[WRAPPER] formula_sources is: ['???.a', '???.b', 'tab.c']
'''

# sql = "ROUND(SUM(a + b - tab.c),2) AS column_vl"
'''
[WRAPPER] formula_alias is: column_vl
[WRAPPER] formula_text is: ROUND(SUM(a + b - tab.c),2)
[WRAPPER] formula_sources is: ['???.a', '???.b', 'tab.c']
'''

# sql = "ROUND(SUM(a + b - tab.c),2) column_vl"
'''
[WRAPPER] formula_alias is: column_vl
[WRAPPER] formula_text is: ROUND(SUM(a + b - tab.c),2)
[WRAPPER] formula_sources is: ['???.a', '???.b', 'tab.c']
'''

# sql = "ROUND(SUM(a + b - tab.c),2) + SUM(tab.a) AS column_vl"
'''
[WRAPPER] formula_alias is: column_vl
[WRAPPER] formula_text is: ROUND(SUM(a + b - tab.c),2)
[WRAPPER] formula_sources is: ['???.a', '???.b', 'tab.c']
'''

# sql = "ROUND(SUM(a + b - tab.c),2) + SUM(tab.a)"
'''
[WRAPPER] formula_alias is: alias#10084
[WRAPPER] formula_text is: ROUND(SUM(a + b - tab.c),2) + SUM(tab.a)
[WRAPPER] formula_sources is: ['???.a', '???.b', 'tab.c', 'tab.a']
'''

# sql = "ROUND(SUM(a + b - tab.c),2) + SUM(tab.a) column_vl"
'''
[WRAPPER] formula_alias is: column_vl
[WRAPPER] formula_text is: ROUND(SUM(a + b - tab.c),2) + SUM(tab.a)
[WRAPPER] formula_sources is: ['???.a', '???.b', 'tab.c', 'tab.a']
'''

# sql = "ROUND(SUM(a + b - tab.c),2) + SUM(tab.a) + tab.b"
'''
[WRAPPER] formula_alias is: alias#83173
[WRAPPER] formula_text is: ROUND(SUM(a + b - tab.c),2) + SUM(tab.a) + tab.b
[WRAPPER] formula_sources is: ['???.a', '???.b', 'tab.c', 'tab.a', 'tab.b']
'''

# sql = "(ROUND(SUM(a + b - tab.c),2) + SUM(tab.a) + tab.b) tab_value_vl"
'''
[WRAPPER] formula_alias is: tab_value_vl
[WRAPPER] formula_text is: (ROUND(SUM(a + b - tab.c),2) + SUM(tab.a) + tab.b)
[WRAPPER] formula_sources is: ['???.a', '???.b', 'tab.c', 'tab.a', 'tab.b']
'''

# sql = "CASE WHEN 1=1 AND 1=0 THEN COALESCE(tab1.col1, tab1.col2, '') WHEN 2=11 THEN '' ELSE tab1.col3 END"
'''
[WRAPPER] formula_alias is: alias#27655
[WRAPPER] formula_text is: CASE WHEN 1=1 AND 1=0 THEN COALESCE(tab1.col1, tab1.col2, '') WHEN 2=11 THEN '' ELSE tab1.col3 END
[WRAPPER] formula_sources is: ['tab1.col1', 'tab1.col2', 'tab1.col3']
'''

# sql = "ROW_NUMBER() OVER (PARTITION BY col1, col2 ORDER BY col3, col4) "
'''
[WRAPPER] formula_alias is: alias#54143
[WRAPPER] formula_text is: ROW_NUMBER() OVER (PARTITION BY col1, col2 ORDER BY col3, col4)
[WRAPPER] formula_sources is: ['???.col1', '???.col2', '???.col3', '???.col4']
'''

# sql = "ROW_NUMBER   () OVER (         PARTITION BY col1         ,col2        ORDER BY col3, col4                             )              "
'''
[WRAPPER] formula_alias is: alias#80787
[WRAPPER] formula_text is: ROW_NUMBER   () OVER (         PARTITION BY col1         ,col2        ORDER BY col3, col4                             )
[WRAPPER] formula_sources is: ['???.col1', '???.col2', '???.col3', '???.col4']
'''

# sql = "LEAD(tab2.key) OVER (PARTITION BY col1, col2 ORDER BY col3, col4)"
'''
[WRAPPER] formula_alias is: alias#55233
[WRAPPER] formula_text is: LEAD(tab2.key) OVER (PARTITION BY col1, col2 ORDER BY col3, col4)
[WRAPPER] formula_sources is: ['tab2.key', '???.col1', '???.col2', '???.col3', '???.col4']
'''

# sql = "SUM(tab2.val1) - avg(tab2.val2) OVER (PARTITION BY col1, col2 ORDER BY col3, col4) "
'''
[WRAPPER] formula_alias is: alias#66168
[WRAPPER] formula_text is: SUM(tab2.val1) - avg(tab2.val2) OVER (PARTITION BY col1, col2 ORDER BY col3, col4)
[WRAPPER] formula_sources is: ['tab2.val1', 'tab2.val2', '???.col1', '???.col2', '???.col3', '???.col4']
'''

# sql = "(tab.key = tub.key)"
'''
[WRAPPER] formula_alias is: alias#92069
[WRAPPER] formula_text is: (tab.key = tub.key)
[WRAPPER] formula_sources is: ['tab.key', 'tub.key']
'''

# sql = "tab.key = COALESCE(tub.key, '') AS ciao"
'''
[WRAPPER] formula_alias is: ciao
[WRAPPER] formula_text is: tab.key = COALESCE(tub.key, '')
[WRAPPER] formula_sources is: ['tab.key', 'tub.key']
'''

test_sql(sql)