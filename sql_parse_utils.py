
import sqlparse


def select_formula_split_renaming(tokens_list):
    '''
    col_alias, col_formula = sql_parse_utils.select_formula_split_renaming(pql[0].tokens[0].tokens)
    '''
    split_idx = 0
    col_alias = ''
    col_formula = list()

    for x in tokens_list:
        if str(x).upper() == 'AS': # caso "{formula} AS {alias}"
            col_alias = tokens_list[-1]
            col_formula = tokens_list[:split_idx-1]
        elif split_idx == len(tokens_list)-1: # caso "{formula} {alias}"
            col_alias = tokens_list[-1]
            col_formula = tokens_list[:-1]
        elif split_idx < len(tokens_list)-1: # continua a cercare
            split_idx += 1
        else:
            col_alias = ''.join([str(x) for x in tokens_list])
    
    return col_alias, col_formula


def select_formula_explode(sql_tokens_object):
    if type(sql_tokens_object) is list:
        return sql_tokens_object
    elif str(type(sql_tokens_object)) in { 
        "<class 'sqlparse.sql.Identifier'>", 
        "<class 'sqlparse.sql.Operation'>", 
        "<class 'sqlparse.sql.Parenthesis'>",
        "<class 'sqlparse.sql.Function'>", 
        "<class 'sqlparse.sql.IdentifierList'>",
        "<class 'sqlparse.sql.Case'>",
        "<class 'sqlparse.sql.Over'>",
        "<class 'sqlparse.sql.Comparison'>",
        }:
        return sql_tokens_object.tokens
    else:
        return sql_tokens_object # anche se è un caso errato


def select_formula_is_identifier(sql_tokens_object):
    return str(type(sql_tokens_object)) == "<class 'sqlparse.sql.Identifier'>"


def select_formula_is_parenthesis(tokens_list, brackets_start='(', brackets_end=')'):
    return len(tokens_list) >= 3 and str(tokens_list[0]) == brackets_start and str(tokens_list[-1]) == brackets_end


def select_formula_is_item_parenthesis(sql_tokens_object):
    return str(type(sql_tokens_object)) == "<class 'sqlparse.sql.Parenthesis'>"


def select_formula_is_item_identifiers_list(sql_tokens_object):
    return str(type(sql_tokens_object)) == "<class 'sqlparse.sql.IdentifierList'>"


def select_formula_is_item_identifier(sql_tokens_object):
    return str(type(sql_tokens_object)) == "<class 'sqlparse.sql.Identifier'>"


def select_formula_is_item_function(sql_tokens_object):
    return str(type(sql_tokens_object)) == "<class 'sqlparse.sql.Function'>"


def select_formula_is_item_comparison(sql_tokens_object):
    return str(type(sql_tokens_object)) == "<class 'sqlparse.sql.Comparison'>"


def select_formula_get_from_parenthesis(tokens_list):
    return tokens_list[1:-1]


def select_formula_is_dot_notation(tokens_list):
    '''
    sql_parse_utils.select_formula_is_dot_notation(pql[0].tokens[0].tokens)
    '''
    tokens_list_types = [str(type(x)) for x in tokens_list]
    expected_tokens_list_types = ["<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>"]
    return len(tokens_list) == 3 and tokens_list_types == expected_tokens_list_types


def select_formula_get_from_dot_notation(tokens_list):
    return f"{tokens_list[0]}.{tokens_list[-1]}"


def select_formula_get_from_single_column_notation(tokens_list):
    return f"{tokens_list[0]}"


def select_formula_is_single_column_notation(tokens_list):
    return len(tokens_list) == 1 and str(type(tokens_list[0]))== "<class 'sqlparse.sql.Token'>"


def select_formula_is_operation(tokens_list):
    return len(tokens_list) == 1 and str(type(tokens_list[0]))== "<class 'sqlparse.sql.Operation'>"


def select_formula_is_simple_function(tokens_list):
    tokens_list_types = [str(type(x)) for x in tokens_list if str(x) != ' ']
    expected_tokens_list_types = [
        "<class 'sqlparse.sql.Identifier'>", 
        "<class 'sqlparse.sql.Parenthesis'>"
        ]
    return len(tokens_list_types) == 2 and tokens_list_types == expected_tokens_list_types


def select_formula_is_window_function(tokens_list):
    '''
    NOTA BENE: Non è necessariamente l'intera window function, poichè l'albero sintattico
    in questo caso potrebbe incorporare la OVER in un nodo FUNCTION o in altro modo. 
    Siccome siamo interessati solo a ricercare delle colonne, non ha molto senso
    entrare nei dettagli, perciò questa funzione semplicemente individua alcuni caratteri
    della window function, anche se magari lo statement è troncato. 
    '''
    tokens_list_types = [str(type(x)) for x in tokens_list if str(x) != ' ']
    expected_tokens_list_types = [
        "<class 'sqlparse.sql.Identifier'>", 
        "<class 'sqlparse.sql.Parenthesis'>", 
        "<class 'sqlparse.sql.Over'>"]
    return len(tokens_list_types) == 3 and tokens_list_types == expected_tokens_list_types


def select_formula_is_item_window_function(sql_tokens_object):
    return str(type(sql_tokens_object)) == "<class 'sqlparse.sql.Over'>"


def select_formula_is_as_statement(tokens_list):
    tokens_list_types = [type(x) for x in tokens_list if str(x) != ' ']
    expected_tokens_list_types = [
        "<class 'sqlparse.sql.Token'>", 
        "<class 'sqlparse.sql.Token'>", 
        "<class 'sqlparse.sql.Identifier'>"
        ]
    return len(tokens_list) == 3 and tokens_list_types == expected_tokens_list_types


def select_formula_is_item_case_statement(sql_tokens_object):
    return str(type(sql_tokens_object)) == "<class 'sqlparse.sql.Case'>"





def sql_is_select_clause(sql_tokens_object):
    return str(type(sql_tokens_object)) == "<class 'sqlparse.sql.Token'>" and str(sql_tokens_object).upper() == 'SELECT'

def sql_is_from_clause(sql_tokens_object):
    return str(type(sql_tokens_object)) == "<class 'sqlparse.sql.Token'>" and str(sql_tokens_object).upper() == 'FROM'

def sql_is_where_clause(sql_tokens_object):
    return str(type(sql_tokens_object)) == "<class 'sqlparse.sql.Where'>" and str(sql_tokens_object).strip().upper().startswith('WHERE')

def sql_is_groupby_clause(sql_tokens_object):
    return str(type(sql_tokens_object)) == "<class 'sqlparse.sql.Token'>" and str(sql_tokens_object).upper() == 'GROUP BY'

def sql_is_having_clause(sql_tokens_object):
    return str(type(sql_tokens_object)) == "<class 'sqlparse.sql.Token'>" and str(sql_tokens_object).upper() == 'HAVING'

def sql_is_orderby_clause(sql_tokens_object):
    return str(type(sql_tokens_object)) == "<class 'sqlparse.sql.Token'>" and str(sql_tokens_object).upper() == 'ORDER BY'

def sql_is_limit_clause(sql_tokens_object):
    return str(type(sql_tokens_object)) == "<class 'sqlparse.sql.Token'>" and str(sql_tokens_object).upper() == 'LIMIT'

def sql_is_clause_keyword(sql_tokens_object):
    return str(sql_tokens_object).upper() in {
        'SELECT', 'FROM', 'QUALIFY', 'GROUP BY', 'HAVING', 'ORDER BY', 'LIMIT'
    } or str(sql_tokens_object).strip().upper().startswith('WHERE')

def sql_is_from_join_keyword(sql_tokens_object):
    return str(sql_tokens_object).upper() in {
        'FROM', 'JOIN', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'FULL JOIN', 'FULL OUTER JOIN', 'FULL INNER JOIN'
    }

def sql_is_blank(sql_tokens_object):
    return str(sql_tokens_object) in { ' ', '\n' }




