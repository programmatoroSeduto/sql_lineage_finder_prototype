
import sqlparse
import sql_parse_utils
import random
import time

random.seed(time.time())





def explore_select_formula(pql_stat):
    '''
    pql_stat : DEVE ESSERE un oggetto sql token, non una lista
    Wrapper layer, serve solo per distinguere i renaming dalle formule secche
    '''
    print(">>> WRAPPER")
    print(pql_stat)
    print(type(pql_stat))

    formula_alias = ''
    formula_text = ''
    formula_sources = list()

    print("[WRAPPER] checking for renamings")
    if sql_parse_utils.select_formula_is_item_identifier(pql_stat):
        pql_stat_inner = sql_parse_utils.select_formula_explode(pql_stat)
        if sql_parse_utils.select_formula_is_as_statement(pql_stat_inner) or (len(pql_stat_inner) > 1 and not sql_parse_utils.select_formula_is_dot_notation(pql_stat_inner)):
            print("\n[WRAPPER] need to resolve renaming")
            pql_stat = sql_parse_utils.select_formula_explode(pql_stat)
            formula_alias, pql_stat = sql_parse_utils.select_formula_split_renaming(pql_stat)
    
    print("[WRAPPER] Starting the explore_select_formula_inner()")
    formula_sources = explore_select_formula_inner(pql_stat, formula_sources=formula_sources)

    if len(formula_sources) == 1 and formula_alias == '':
        formula_alias = formula_sources[0].split('.')[-1]

    print("\n\n")
    
    if formula_alias == '':
        formula_alias = f"alias#{random.randint(10000, 99999)}"
    print("[WRAPPER] formula_alias is:", formula_alias)
    
    if formula_text == '':
        formula_text = ''.join([str(x) for x in pql_stat]).strip()
    print("[WRAPPER] formula_text is:", formula_text)
    
    print(f"[WRAPPER] formula_sources is: {formula_sources}")

    return formula_alias, formula_text, formula_sources







def explore_select_formula_inner(pql, formula_sources=list()):
    print(f"\n>>> ITERATION on '{pql}'")

    pql_stat = sql_parse_utils.select_formula_explode(pql)
    print(pql_stat)
    print(type(pql_stat))

    if sql_parse_utils.select_formula_is_window_function(pql_stat):
        print(f"[ITERATION]", pql_stat, "--> IS WINDOW FUNCTION")
        return explore_select_formula_inner(
            pql_stat[1:], 
            formula_sources=formula_sources)

    elif sql_parse_utils.select_formula_is_simple_function(pql_stat):
        print(f"[ITERATION]", pql_stat, "--> IS SIMPLE FUNCTION")
        return explore_select_formula_inner(
            pql_stat[1], 
            formula_sources=formula_sources)

    elif sql_parse_utils.select_formula_is_operation(pql_stat):
        print(f"[ITERATION]", pql_stat, "--> IS OPERATION NOTATION")
        return explore_select_formula_inner(
            pql_stat[0], 
            formula_sources=formula_sources)

    elif sql_parse_utils.select_formula_is_dot_notation(pql_stat):
        print(f"[ITERATION]", pql_stat, "--> IS DOT NOTATION")
        formula_sources.append(
            sql_parse_utils.select_formula_get_from_dot_notation(pql_stat)
        )

    elif sql_parse_utils.select_formula_is_single_column_notation(pql_stat):
        print(f"[ITERATION]", pql_stat, "--> IS COLUMN NOTATION")
        formula_sources.append(
            '???.' + sql_parse_utils.select_formula_get_from_single_column_notation(pql_stat)
        )
    
    else:
        print(f"[ITERATION]", pql_stat, "--> need to iterate on single objects")
        return explore_select_formula_inner_items(
            pql_stat,
            formula_sources=formula_sources,
        )

    return formula_sources







def explore_select_formula_inner_items(pql_stat, formula_sources=list()):
    '''
    pql_stat : lista di items sql
    '''
    for pql_item in pql_stat:
        if str(type(pql_item)) == "<class 'sqlparse.sql.Token'>":
            print(f"[ITERATION] skipping item '{pql_item}' (is Token object)")
            continue
        
        elif str(pql_stat).upper == 'AS':
            return None
        
        elif sql_parse_utils.select_formula_is_identifier(pql_item):
            formula_sources = explore_select_formula_inner(
                pql_item, 
                formula_sources=formula_sources
                )
            
        elif sql_parse_utils.select_formula_is_single_column_notation([pql_item, ]):
            formula_sources = explore_select_formula_inner(
                pql_item, 
                formula_sources=formula_sources
                )
        
        elif sql_parse_utils.select_formula_is_operation([pql_item, ]):
            formula_sources = explore_select_formula_inner(
                pql_item, 
                formula_sources=formula_sources
                )
        
        elif sql_parse_utils.select_formula_is_item_parenthesis(pql_item):
            formula_sources = explore_select_formula_inner(
                pql_item, 
                formula_sources=formula_sources
                )
        
        elif sql_parse_utils.select_formula_is_item_function(pql_item):
            formula_sources = explore_select_formula_inner(
                pql_item, 
                formula_sources=formula_sources
                )
        
        elif sql_parse_utils.select_formula_is_item_identifiers_list(pql_item):
            formula_sources = explore_select_formula_inner(
                pql_item, 
                formula_sources=formula_sources
                )
        
        elif sql_parse_utils.select_formula_is_item_case_statement(pql_item):
            formula_sources = explore_select_formula_inner(
                pql_item, 
                formula_sources=formula_sources
                )
        
        elif sql_parse_utils.select_formula_is_item_window_function(pql_item):
            formula_sources = explore_select_formula_inner(
                pql_item, 
                formula_sources=formula_sources
                )
        
        elif sql_parse_utils.select_formula_is_item_comparison(pql_item):
            formula_sources = explore_select_formula_inner(
                pql_item, 
                formula_sources=formula_sources
                )
        
        else:
            print(f"[ITERATION] skipping item '{pql_item}' wiith type {type(pql_item)} (is something else)")
            continue
    
    return formula_sources