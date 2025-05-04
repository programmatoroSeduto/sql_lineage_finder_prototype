import sqlparse
import json

sql = ''
with open(
    './sql_examples/example_simple_03.sql', 
    'r',
) as fil:
    sql = fil.read()

def tokens(token_source):
    return [x for x in token_source if not x.is_whitespace]

print("============ SQL ============")
print(sql)
print("============ SQL ============")

print("============ PARSER RAW ============")
pql = tokens(sqlparse.parse(sql)[0])
print(pql)
for idx, item in enumerate(pql):
    print(f"[{idx}] =====")
    print(pql[idx])
    print("type:", type(pql[idx]))
print("============ PARSER RAW ============")

print("============ SQL TO JSON ============")
def split_name_formula(pql, use_point_split=True):
    tk = tokens(pql)
    if len(tk) == 1:
        if use_point_split and '.' in str(tk[0]):
            return str(tk[0]).split('.')[-1], tk
        else: 
            return str(tk[0]), list()
    else:
        return str(tk[-1]), tk


def interpret_select(pql, idx, source_layer=0):
    found_columns = dict()
    tk = tokens(pql[idx])
    for tkk in tk:
        if str(type(tkk)) == "<class 'sqlparse.sql.Identifier'>":
            col_name, col_formula = split_name_formula(tkk)
            found_columns[col_name] = {
                'source_layer' : source_layer,
                'formula' : col_formula,
            }
    return idx + 1, found_columns


def interpret_from(pql, idx, layers):
    found_tables = dict()
    tk = tokens(pql[idx])
    
    from_layer = 0
    table_name = ''
    table_subquery = ''
    if len(tk) == 1:
        table_name = str(tk[0])
        table_subquery = ''
    else:
        table_name = str(tk[-1])
        table_subquery = str(tk[0])
    
    found_tables[table_name] = {
        'from_layer' : from_layer,
        'subquery' : table_subquery,
        'sources_count' : 0,
    }

    return idx + 1, found_tables, layers


def interpret_group_by(pql, idx):
    group_by_clause = [x for x in tokens(pql[idx]) if str(x) != ',']
    return idx + 1, group_by_clause


def interpret_having(pql, idx):
    having_clause = list()
    tk = pql[idx]

    while str(tk).upper() not in ( 'ORDER BY', 'LIMIT' ) and idx < len(pql):
        having_clause.append(tk)
        idx += 1
        tk = pql[idx]
    return idx + 1, having_clause


def analyze(pql, layers=list(), columns=dict(), tables=dict(), group_by_clause=list(), having_clause=list()):
    idx = 0
    while True:
        tk = pql[idx]
        
        idx += 1
        if str(tk).upper() == 'SELECT':
            idx, columns = interpret_select(pql, idx)
        elif str(tk).upper() == 'FROM':
            idx, tables, layers = interpret_from(pql, idx, layers)
        elif str(tk).upper() == 'GROUP BY':
            idx, group_by_clause = interpret_group_by(pql, idx)
        elif str(tk).upper() == 'HAVING':
            idx, having_clause = interpret_having(pql, idx)
        
        if idx == len(pql):
            break

    print("found_columns:", columns)
    print("found_tables:", tables)
    print("group_by_clause:", group_by_clause)
    print("having_clause:", having_clause)

analyze(pql, layers=['root',])
print("============ SQL TO JSON ============")