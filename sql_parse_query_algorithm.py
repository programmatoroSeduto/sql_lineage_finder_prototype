
import sqlparse
import sql_parse_utils
from sql_parse_formula_algorithm import explore_select_formula
import random
import time

random.seed(time.time())




def explore_sql_statement(pql_stat):
    '''
    pql: una lista di token che rappresenta la sequenza dello statement SQL

    La funzione esplora sequenzialmente tutte le clausole SQL
    SELECT ...
    FROM ...
    WHERE ...
    GROUP BY ...
    HAVING ...
    QUALITY ...
    ORDER BY ...
    LIMIT ...
    '''

    print(f">>> [SQL explore]")
    print(pql_stat)

    clause_select = list()
    clause_from = list()
    clause_where = list()
    clause_groupby = list()
    clause_having = list()
    clause_orderby = list()
    clause_limit = list()

    idx = 0
    # for sql_tokens_object in pql_stat:
    while idx < len(pql_stat):
        sql_tokens_object = pql_stat[idx]
        idx = idx + 1

        if sql_parse_utils.sql_is_select_clause(sql_tokens_object):
            print(f"[SQL explore] found SELECT clause")
            clause_select, idx = explore_sql_statement_clause(pql_stat, idx, clean_blanks=True, clause_content=clause_select)
            print("clause_select:", clause_select)
            print()

        elif sql_parse_utils.sql_is_from_clause(sql_tokens_object):
            print(f"[SQL explore] found FROM clause")
            clause_from.append(sql_tokens_object)
            clause_from, idx = explore_sql_statement_clause(pql_stat, idx, clause_content=clause_from)
            clause_from = explore_from_clause(clause_from)
            print("clause_from:", clause_from)
            print()

        elif sql_parse_utils.sql_is_where_clause(sql_tokens_object):
            print(f"[SQL explore] found WHERE clause")
            clause_where.append(sql_tokens_object)
            print("clause_where:", clause_where)
            print()

        elif sql_parse_utils.sql_is_groupby_clause(sql_tokens_object):
            print(f"[SQL explore] found GROUP BY clause")
            print(idx)
            print(sql_tokens_object)
            clause_groupby.append(sql_tokens_object)
            clause_groupby, idx = explore_sql_statement_clause(pql_stat, idx, clause_content=clause_groupby)
            print("clause_groupby:", clause_groupby)
            print()

        elif sql_parse_utils.sql_is_having_clause(sql_tokens_object):
            print(f"[SQL explore] found HAVING clause")
            clause_having.append(sql_tokens_object)
            clause_having, idx = explore_sql_statement_clause(pql_stat, idx, clause_content=clause_having)
            print("clause_having:", clause_having)
            print()

        elif sql_parse_utils.sql_is_orderby_clause(sql_tokens_object):
            print(f"[SQL explore] found ORDER BY clause")
            clause_orderby.append(sql_tokens_object)
            clause_orderby, idx = explore_sql_statement_clause(pql_stat, idx, clause_content=clause_orderby)
            print("clause_orderby:", clause_orderby)
            print()

        elif sql_parse_utils.sql_is_limit_clause(sql_tokens_object):
            print(f"[SQL explore] found LIMIT clause")
            clause_limit.append(sql_tokens_object)
            clause_limit, idx = explore_sql_statement_clause(pql_stat, idx, clause_content=clause_limit)
            print("clause_limit:", clause_limit)
            print()
    
    return clause_select, clause_from, clause_where, clause_groupby, clause_having, clause_orderby, clause_limit






def explore_sql_statement_clause(pql_stat, idx, clean_blanks=False, clause_content=list()):
    '''
    ritorna la lista di elementi trovati sotto la clausola
    più l'indice, che punta direttamente al prossimo token da consumare
    '''
    
    while idx < len(pql_stat):
        sql_tokens_object = pql_stat[idx]
        idx = idx + 1

        if clean_blanks and sql_parse_utils.sql_is_blank(sql_tokens_object):
            continue
        elif not sql_parse_utils.sql_is_clause_keyword(sql_tokens_object):
            clause_content.append(sql_tokens_object)
        else:
            break

    return clause_content, idx-1








def explore_from_clause(pql_stat, clean_statement=False):
    '''
    pql: una lista di token che rappresenta la sequenza della sola parte FROM nello statement SQL
    '''
    from_clause_parts = list() # of parts
    
    part = list()
    for sql_tokens_object in pql_stat:
        if clean_statement and sql_parse_utils.sql_is_blank(sql_tokens_object):
            continue
        if sql_parse_utils.sql_is_from_join_keyword(sql_tokens_object):
            if len(part) > 0:
                from_clause_parts.append(part)
            part = list()
            part.append(sql_tokens_object)
        else:
            part.append(sql_tokens_object)
    from_clause_parts.append(part)
    
    return from_clause_parts




def explore_from_clause_part(pql_stat, found_tables=dict(), found_columns=list()):
    '''
    La clausola deve soddisfare le proprietà:
    - dev'essere lunga 4 dopo essere stata ripulita
    - il primo elemento dev'essere una keyword dello statement FROM
    - il secondo e il quarto elemento devono essere quelli che si portano dietro la info
    '''
    pql_stat = [x for x in pql_stat if not sql_parse_utils.sql_is_blank(x)]
    print(pql_stat)

    is_main_from = str(pql_stat[0]).upper() == 'FROM'
    is_using_join = len(pql_stat) == 4 and str(pql_stat[2]).upper() == 'USING'

    table_name = ''
    table_definition = list()
    table_join_formula = list()
    table_found_columns = list()

    # il primo identifier è comune a tutti
    table_name, str(pql_stat[0])
    table_definition = pql_stat[1]

    if not is_main_from:
        table_join_formula = pql_stat[-1]
        if is_using_join:
            raise NotImplementedError("La USING necessita di un'attenzione maggiore, ancora da implementare, non usare")
            # _, table_join_formula, table_found_columns = explore_select_formula(table_join_formula)
        else:
            _, table_join_formula, table_found_columns = explore_select_formula(table_join_formula)

    return table_name, table_definition, table_join_formula, table_found_columns