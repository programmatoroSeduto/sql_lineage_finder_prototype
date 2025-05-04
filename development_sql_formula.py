
import sql_parse_utils
import sqlparse
from sql_parse_formula_algorithm import explore_select_formula, explore_select_formula_inner


sql = "col1"
pql = sqlparse.parse(sql)
print("=====")
print("Formula SELECT:")
print(sql)
print(pql[0].tokens)
print(type(pql[0].tokens[0]))
print("è un gruppo?", pql[0].tokens[0].is_group)
print("Esplodo l'oggetto, dato che è un gruppo:")
print(pql[0].tokens[0].tokens)
print(type(pql[0].tokens[0].tokens[0]))
print(f"soddisfa la dot notation?", sql_parse_utils.select_formula_is_dot_notation(pql[0].tokens[0].tokens))
print(f"soddisfa la single column notation?", sql_parse_utils.select_formula_is_single_column_notation(pql[0].tokens[0].tokens))
print("source della formula:")
print(pql[0].tokens[0].tokens[0])

sql = "tab1.col1"
pql = sqlparse.parse(sql)
print("=====")
print("Formula SELECT:")
print(sql)
print(pql[0].tokens)
print("E' un identifier, caso 1; esplodo l'identifier")
print(pql[0].tokens[0].tokens)
print("Posso riconoscere una DOT notation direttamente guardando la lista di tipi")
print([str(type(x)) for x in pql[0].tokens[0].tokens])
print(f"soddisfa la dot notation?", sql_parse_utils.select_formula_is_dot_notation(pql[0].tokens[0].tokens))
print(f"source della formula: {pql[0].tokens[0].tokens[0]}.{pql[0].tokens[0].tokens[2]}")

sql = "col1 AS column_alias"
pql = sqlparse.parse(sql)
print("=====")
print("Formula SELECT:")
print(sql)
print(pql[0].tokens)
print("esplodo l'oggetto")
print(pql[0].tokens[0].tokens)
print(f"soddisfa la dot notation?", 
      sql_parse_utils.select_formula_is_dot_notation(pql[0].tokens[0].tokens))
print(f"soddisfa la single column notation?", 
      sql_parse_utils.select_formula_is_single_column_notation(pql[0].tokens[0].tokens))
print("l'oggetto non soddisfa i due passi base, quindi scatta la normalizzazione")
col_alias, col_formula = sql_parse_utils.select_formula_split_renaming(pql[0].tokens[0].tokens)
print(f"Nome della variabile: {col_alias}")
print("Post normalizzazione:")
print(col_formula)
print("REITERO l'algoritmo su quello che rimane. In questo caso, ho direttamente l'oggetto Token")
print(f"soddisfa la dot notation?", 
      sql_parse_utils.select_formula_is_dot_notation(col_formula))
print(f"soddisfa la single column notation?", 
      sql_parse_utils.select_formula_is_single_column_notation(col_formula))
print(f"source della formula: {col_formula[0]}")


sql = "tab.b AS column_b"
pql = sqlparse.parse(sql)
print("=====")
print("Formula SELECT:")
print(sql)
print(pql[0].tokens)
print("esplodo l'identifier")
pql_stat = sql_parse_utils.select_formula_explode(pql[0].tokens[0])
print(pql_stat)
print(f"soddisfa la dot notation?", 
      sql_parse_utils.select_formula_is_dot_notation(pql_stat))
print(f"soddisfa la single column notation?", 
      sql_parse_utils.select_formula_is_single_column_notation(pql_stat))
print("Non soddisfa entrambe le condizioni, quindi procedi alla SPLIT")
col_alias, col_formula = sql_parse_utils.select_formula_split_renaming(pql[0].tokens[0].tokens)
print("FOUND IDENTIFIER:", col_alias)
print("la sua formula è")
print(col_formula)
print("REITERO esplodo l'identifier")
pql_stat = sql_parse_utils.select_formula_explode(col_formula)
print(pql_stat)
print(f"soddisfa la dot notation?", 
      sql_parse_utils.select_formula_is_dot_notation(col_formula))
print(f"soddisfa la single column notation?", 
      sql_parse_utils.select_formula_is_single_column_notation(col_formula))
print("Soddisfa la DOT notation! Source -->",
      sql_parse_utils.select_formula_get_from_dot_notation(col_formula))


sql = "tab.a + b AS value_vl"
pql = sqlparse.parse(sql)
print("=====")
print("Formula SELECT:")
print(sql)
print(pql[0].tokens)
print("\n>>> WRAPPER: esplodo e verifico")
pql_stat = sql_parse_utils.select_formula_explode(pql[0].tokens[0])
print(pql_stat)
print(f"soddisfa la dot notation?", 
      sql_parse_utils.select_formula_is_dot_notation(pql_stat))
print(f"soddisfa la single column notation?", 
      sql_parse_utils.select_formula_is_single_column_notation(pql_stat))
print(f"soddisfa la operation?", 
      sql_parse_utils.select_formula_is_operation(pql_stat))
print("Non soddisfa nessuna delle tre, quindi splitto e itero perchè ci sarà sicuramente un AS; è proprio per gestire questa casistica che esiste il wrapper dell'algoritmo. ")
col_alias, pql_stat = sql_parse_utils.select_formula_split_renaming(pql_stat)
print("alias-->", col_alias)
print("formula-->", ''.join([str(x) for x in pql_stat]))
print("\n>>> ITERAZIONE 0: eplodo e verifico")
pql_stat = sql_parse_utils.select_formula_explode(pql_stat)
print(pql_stat)
print(f"soddisfa la dot notation?", 
      sql_parse_utils.select_formula_is_dot_notation(pql_stat))
print(f"soddisfa la single column notation?", 
      sql_parse_utils.select_formula_is_single_column_notation(pql_stat))
print(f"soddisfa la operation?", 
      sql_parse_utils.select_formula_is_operation(pql_stat))
print("è una operation! Itero su questa")
print("\n>>> ITERAZIONE 1: eplodo e verifico")
pql_stat = sql_parse_utils.select_formula_explode(pql_stat[0])
print(pql_stat)
print(f"soddisfa la dot notation?", 
      sql_parse_utils.select_formula_is_dot_notation(pql_stat))
print(f"soddisfa la single column notation?", 
      sql_parse_utils.select_formula_is_single_column_notation(pql_stat))
print(f"soddisfa la operation?", 
      sql_parse_utils.select_formula_is_operation(pql_stat))
print("Nessuna delle tre condizioni è soddisfatta, quindi passo a smazzare elemento per elemento")
print("FOREACH item IN tokens_list")
print("[0] è un identifier?", sql_parse_utils.select_formula_is_identifier(pql_stat[0]), "--> REITERO ed esplodo il caso --> is dot?", sql_parse_utils.select_formula_is_dot_notation(pql_stat[0].tokens))
print("[1] è un identifier?", sql_parse_utils.select_formula_is_identifier(pql_stat[1]))
print("[2] è un identifier?", sql_parse_utils.select_formula_is_identifier(pql_stat[2]))
print("[3] è un identifier?", sql_parse_utils.select_formula_is_identifier(pql_stat[3]))
print("[4] è un identifier?", sql_parse_utils.select_formula_is_identifier(pql_stat[4]), "--> REITERO ed esplodo il caso --> is col?", sql_parse_utils.select_formula_is_single_column_notation(pql_stat[4].tokens))
print("Per ognuna delle sorgenti individuate dal passo base, vado ad aggiungere una source")


sql = "tab.a + b + (tab2.c/d) AS col_vl"
pql = sqlparse.parse(sql)
print(sql)
print(pql[0].tokens)
print("\n>>> WRAPPER: esplodo e verifico")
pql_stat = sql_parse_utils.select_formula_explode(pql[0].tokens[0])
print(pql_stat)
print(f"soddisfa la dot notation?", 
      sql_parse_utils.select_formula_is_dot_notation(pql_stat))
print(f"soddisfa la single column notation?", 
      sql_parse_utils.select_formula_is_single_column_notation(pql_stat))
print(f"soddisfa la operation?", 
      sql_parse_utils.select_formula_is_operation(pql_stat))
print("Non soddisfa nessuna delle tre, quindi splitto e itero perchè ci sarà sicuramente un AS; è proprio per gestire questa casistica che esiste il wrapper dell'algoritmo. ")
col_alias, pql_stat = sql_parse_utils.select_formula_split_renaming(pql_stat)
print("alias-->", col_alias)
print("\n>>> ITERAZIONE 0: eplodo e verifico")
pql_stat = sql_parse_utils.select_formula_explode(pql_stat)
print(pql_stat)
print(f"soddisfa la dot notation?", 
      sql_parse_utils.select_formula_is_dot_notation(pql_stat))
print(f"soddisfa la single column notation?", 
      sql_parse_utils.select_formula_is_single_column_notation(pql_stat))
print(f"soddisfa la operation?", 
      sql_parse_utils.select_formula_is_operation(pql_stat))
print("è una operation! Itero su questa")
pql_stat = pql_stat[0]
print("\n>>> ITERAZIONE 1: eplodo e verifico")
pql_stat = sql_parse_utils.select_formula_explode(pql_stat)
print(pql_stat)
print(f"soddisfa la dot notation?", 
      sql_parse_utils.select_formula_is_dot_notation(pql_stat))
print(f"soddisfa la single column notation?", 
      sql_parse_utils.select_formula_is_single_column_notation(pql_stat))
print(f"soddisfa la operation?", 
      sql_parse_utils.select_formula_is_operation(pql_stat))
print(f"soddisfa la parenthesis?", 
      sql_parse_utils.select_formula_is_parenthesis(pql_stat))
print("Qui compare l'oggetto parenthesis, e l'operator contiene a sua volta un altro operator da esplodere")
print("Supponiamo di iterare elemento per elemento")
pql_stat = pql_stat[-1]
print("\n>>> ITERAZIONE 2: eplodo e verifico")
pql_stat = sql_parse_utils.select_formula_explode(pql_stat)
print(pql_stat)
print(f"soddisfa la dot notation?", 
      sql_parse_utils.select_formula_is_dot_notation(pql_stat))
print(f"soddisfa la single column notation?", 
      sql_parse_utils.select_formula_is_single_column_notation(pql_stat))
print(f"soddisfa la operation?", 
      sql_parse_utils.select_formula_is_operation(pql_stat))
print(f"soddisfa la parenthesis?", 
      sql_parse_utils.select_formula_is_parenthesis(pql_stat))
print("REITERO sul contenuto delle brackets")
pql_stat = sql_parse_utils.select_formula_get_from_parenthesis(pql_stat)
print("\n>>> ITERAZIONE 2: eplodo e verifico")
pql_stat = sql_parse_utils.select_formula_explode(pql_stat)
print(pql_stat)
print(f"soddisfa la dot notation?", 
      sql_parse_utils.select_formula_is_dot_notation(pql_stat))
print(f"soddisfa la single column notation?", 
      sql_parse_utils.select_formula_is_single_column_notation(pql_stat))
print(f"soddisfa la operation?", 
      sql_parse_utils.select_formula_is_operation(pql_stat))
print(f"soddisfa la parenthesis?", 
      sql_parse_utils.select_formula_is_parenthesis(pql_stat))
print("Per le operation: esplodo sulle operaions fino al passo base")
print("per le brackets: spacchetto ed esplodo alla successiva iterazione")


sql = "SUM(a)"
pql = sqlparse.parse(sql)
print(sql)
print(pql[0].tokens)
print("\n>>> WRAPPER: esplodo e verifico")
pql_stat = sql_parse_utils.select_formula_explode(pql[0].tokens)
print(pql_stat)
print(f"soddisfa la dot notation?", 
      sql_parse_utils.select_formula_is_dot_notation(pql_stat))
print(f"soddisfa la single column notation?", 
      sql_parse_utils.select_formula_is_single_column_notation(pql_stat))
print(f"soddisfa la operation?", 
      sql_parse_utils.select_formula_is_operation(pql_stat))
print("Qui compare la function")
print(pql[0].tokens[0])
print(type(pql[0].tokens[0]))
pql_stat = pql[0].tokens[0]
print(f"soddisfa la function?", 
      sql_parse_utils.select_formula_is_item_function(pql_stat))
print("\n>>> ITERAZIONE 2: eplodo e verifico")
pql_stat = sql_parse_utils.select_formula_explode(pql_stat)
print(pql_stat)
print(f"soddisfa la dot notation?", 
      sql_parse_utils.select_formula_is_dot_notation(pql_stat))
print(f"soddisfa la single column notation?", 
      sql_parse_utils.select_formula_is_single_column_notation(pql_stat))
print(f"soddisfa la operation?", 
      sql_parse_utils.select_formula_is_operation(pql_stat))
print([str(type(x)) for x in pql_stat])





sql = "col AS column_vl"
pql = sqlparse.parse(sql)
print("=====")
print(sql)
print(pql[0].tokens)
print(type(pql[0].tokens[0]))
print([x for x in pql[0].tokens[0].tokens if str(x) != ' '])
print([str(type(x)) for x in [x for x in pql[0].tokens[0].tokens if str(x) != ' ']])




sql = "CASE WHEN 1=1 AND 1=0 THEN COALESCE(tab1.col1, tab1,col2, '') WHEN 2=11 THEN '' ELSE tab1.col3 END"
pql = sqlparse.parse(sql)
print("=====")
print(sql)
print(pql[0].tokens)
print(type(pql[0].tokens[0]))
'''
[<Case 'CASE W...' at 0x23C3E98A270>]
<class 'sqlparse.sql.Case'>
'''
print([x for x in pql[0].tokens[0].tokens if str(x) != ' '])
'''
[<Keyword 'CASE' at 0x21E540C1B20>, <Whitespace ' ' at 0x21E540C1B80>, <Keyword 'WHEN' at 0x21E540C1BE0>, <Whitespace ' ' at 0x21E540C1C40>, <Comparison '1=1' at 0x21E540C0F20>, <Whitespace ' ' at 0x21E540C1DC0>, <Keyword 'AND' at 0x21E540C1E20>, <Whitespace ' ' at 0x21E540C1E80>, <Comparison '1=0' at 0x21E540C0EB0>, <Whitespace ' ' at 0x21E540C4040>, <Keyword 'THEN' at 0x21E540C40A0>, <Whitespace ' ' at 0x21E540C4100>, <Function 'COALES...' at 0x21E540C0CF0>, <Whitespace ' ' at 0x21E540C46A0>, <Keyword 'WHEN' at 0x21E540C4700>, <Whitespace ' ' at 0x21E540C4760>, <Comparison '2=11' at 0x21E540C5190>, <Whitespace ' ' at 0x21E540C48E0>, <Keyword 'THEN' at 0x21E540C4940>, <Whitespace ' ' at 0x21E540C49A0>, <Single "''" at 0x21E540C4A00>, <Whitespace ' ' at 0x21E540C4A60>, <Keyword 'ELSE' at 0x21E540C4AC0>, <Whitespace ' ' at 0x21E540C4B20>, <Identifier 'tab1.c...' at 0x21E540C0E40>, <Whitespace ' ' at 0x21E540C4CA0>, <Keyword 'END' at 0x21E540C4D00>]
'''



sql = "ROW_NUMBER() OVER (PARTITION BY col1, col2 ORDER BY col3, col4) "
pql = sqlparse.parse(sql)
print("=====")
print(sql)
print(pql[0].tokens)
print(type(pql[0].tokens[0]))
print(pql[0].tokens[0].tokens)
'''
[<Identifier 'ROW_NU...' at 0x1B4166A5510>, <Parenthesis '()' at 0x1B4166A5270>, <Whitespace ' ' at 0x1B4166A4FA0>, <Over 'OVER (...' at 0x1B4166A5350>]
'''
print([str(type(x)) for x in pql[0].tokens[0].tokens if str(x) != ' '])
'''
["<class 'sqlparse.sql.Identifier'>", "<class 'sqlparse.sql.Parenthesis'>", "<class 'sqlparse.sql.Over'>"]
'''




sql = "SUM(tab2.val1) - avg(tab2.val2) OVER (PARTITION BY col1, col2 ORDER BY col3, col4) "
pql = sqlparse.parse(sql)
print("=====")
print(sql)
print(pql[0].tokens)
print(type(pql[0].tokens[0]))
print(pql[0].tokens[0].tokens)
'''
[<Function 'SUM(ta...' at 0x1D72407E120>, <Whitespace ' ' at 0x1D72407B580>, <Operator '-' at 0x1D72407B5E0>, <Whitespace ' ' at 0x1D72407B640>, <Function 'avg(ta...' at 0x1D72407E200>]
'''
print([str(type(x)) for x in pql[0].tokens[0].tokens if str(x) != ' '])
'''
["<class 'sqlparse.sql.Function'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Function'>"]
'''
print(pql[0].tokens[0].tokens[4].tokens)
'''
[<Identifier 'avg' at 0x1E01FE5E430>, <Parenthesis '(tab2....' at 0x1E01FE58F90>, <Whitespace ' ' at 0x1E01FE5B8E0>, <Over 'OVER (...' at 0x1E01FE5E040>]
'''
print([str(type(x)) for x in pql[0].tokens[0].tokens[4].tokens if str(x) != ' '])
'''
["<class 'sqlparse.sql.Identifier'>", "<class 'sqlparse.sql.Parenthesis'>", "<class 'sqlparse.sql.Over'>"]
'''
print(pql[0].tokens[0].tokens[4].tokens[3].tokens)
'''
[<Keyword 'OVER' at 0x1A345D0B940>, <Whitespace ' ' at 0x1A345D0B9A0>, <Parenthesis '(PARTI...' at 0x1A345D08EB0>]
'''
print([str(type(x)) for x in pql[0].tokens[0].tokens[4].tokens[3].tokens if str(x) != ' '])
'''
["<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Parenthesis'>"]
'''
print(pql[0].tokens[0].tokens[4].tokens[3].tokens[2].tokens)




sql = "LEAD(tab2.key) OVER (PARTITION BY col1, col2 ORDER BY col3, col4) "
pql = sqlparse.parse(sql)
print("=====")
print(sql)
print(pql[0].tokens)
print(type(pql[0].tokens[0]))
print(pql[0].tokens[0].tokens)
'''
[<Identifier 'LEAD' at 0x1E7A15B6AC0>, <Parenthesis '(tab2....' at 0x1E7A15B6900>, <Whitespace ' ' at 0x1E7A15B8A60>, <Over 'OVER (...' at 0x1E7A15B69E0>]
'''
print([str(type(x)) for x in pql[0].tokens[0].tokens if str(x) != ' '])
'''
["<class 'sqlparse.sql.Identifier'>", "<class 'sqlparse.sql.Parenthesis'>", "<class 'sqlparse.sql.Over'>"]
'''



sql = "(tab.key = tub.key)"
pql = sqlparse.parse(sql)
print("=====")
print(sql)
print(pql[0].tokens)
print(type(pql[0].tokens[0]))
print(pql[0].tokens[0].tokens)
print(pql[0].tokens[0].tokens[1].tokens)
print(type(pql[0].tokens[0].tokens[1]))