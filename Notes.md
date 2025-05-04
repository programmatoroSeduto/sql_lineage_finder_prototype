# SQL lineage inspector

## Online Available SQL parsers

Parser 1:

- [sqlparse ReadTheDocs](https://sqlparse.readthedocs.io/en/latest/)

```sh
pip install sqlparse
```

Parser 2:

- [sql-metadata](https://github.com/macbre/sql-metadata/blob/master/README.md)

```
pip install sql-metadata
```

## A complex query example

```sql
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
FROM tab
WHERE 1=1
    AND rowno BETWEEN 26 AND 567
LIMIT 100 
)

SELECT 
dim, 
SUM(kpi_converted) AS kpi_final
FROM tab_pre_final

WHERE dim <> '' AND dim IS NOT NULL AND dim <> 'NON USARE'
GROUP BY dim
HAVING SUM(kpi_converted) BETWEEN 50 AND 5000
ORDER BY kpi_final, dim
LIMIT 1
```


## Using Parser 1

```py
import sqlparse
```

Funziona con un meccanismo abbastanza interessante di traversing tramite il campo `tokens`. Il campo fornisce una lista, che segue la conformazione del codice SQL e permette di ottenere facilmente tutti i nomi iterando. 

E' quello più indicato secondo me per un'applicazione stabile professionale. 

### Using Parser 2

Carino, ma richiede uno step di parsing a mano, molto scomodo. Il primo invece ha un lexer degno di questo nome. 


## Guida veloce a sqlparse

Dato un codice SQL, vedi quello complesso sopra, si crea l'oggetto principale: 

```py
sql = "WITH tab AS ( ..."

pql = sqlparse.parse(sql) # <class 'tuple'>
# tupla che contiene tutti gli statement SQL della transazione
```

Lo statement SQL può anche essere una transazione complessa. L'oggetto tupla conterrà tutte le query individuate. In questo esempio, la transazione è composta di una sola query, 

```py
print(pql)
# (<Statement ' WITH ...' at 0x21D227AB120>,)

print(type(pql[0]))
# <class 'sqlparse.sql.Statement'>
```

Per vedere cosa c'è all'interno, fai traversing su `.tokens`:

```py
pql_stat = pql[0]

print(pql_stat.tokens)
# [<Newline ' ' at 0x23599A908E0>, <CTE 'WITH' at 0x23599A90940>, <Whitespace ' ' at 0x23599A909A0>, <Newline ' ' at 0x23599A90A00>, <Newline ' ' at 0x23599A90A60>, <Identifier 'tab AS...' at 0x23599A94E40>, <Newline ' ' at 0x23599A90CA0>, <DML 'SELECT' at 0x23599A90D00>, <Whitespace ' ' at 0x23599A90D60>, <Newline ' ' at 0x23599A90DC0>, <IdentifierList 'ROW_NU...' at 0x23599AA4EB0>, <Newline ' ' at 0x23599A9C160>, <Keyword 'FROM' at 0x23599A9C1C0>, <Whitespace ' ' at 0x23599A9C220>, <Identifier 'sch_ra...' at 0x23599A94AC0>, <Newline ' ' at 0x23599A9C520>, <Keyword 'LEFT J...' at 0x23599A9C580>, <Whitespace ' ' at 0x23599A9C5E0>, <Identifier 'sch_ra...' at 0x23599A94B30>, <Newline ' ' at 0x23599A9C8E0>, <Keyword 'ON' at 0x23599A9C940>, <Whitespace ' ' at 0x23599A9C9A0>, <Parenthesis '( fn.c...' at 0x23599A94510>, <Newline ' ' at 0x23599A9EB20>, <Newline ' ' at 0x23599A9EB80>, <DML 'SELECT' at 0x23599A9EBE0>, <Whitespace ' ' at 0x23599A9EC40>, <Newline ' ' at 0x23599A9ECA0>, <IdentifierList 'MIN(ro...' at 0x23599AA8120>, <Newline ' ' at 0x23599AA0EE0>, <Keyword 'FROM' at 0x23599AA0F40>, <Whitespace ' ' at 0x23599AA0FA0>, <Identifier 'tab' at 0x23599AA49E0>, <Newline ' ' at 0x23599AA10A0>]
```

E' interessante notare che la query viene tokenizzata per più passaggi: il primo step è tokenizzare a grandi linee, quindi ad esempio 

- WITH
  - SELECT 
  - tutti i campi della select
  - FROM 
  - primo from
  - LEFT JOIN con seconda source
  - ON e la condizione intera
- SELECT 
  - tutti i campi della seect
  - FROM 
  - primo from

Il parser tende a non spacchettare le singole sezioni, a meno che venga richiesto chiamando su di esse `.tokens`, e comunque non spacchetta mai interamente le funzioni. 


### Manipolazione del singolo token

Prendiamo l'elemento `<Whitespace ' ' at 0x2C951755A60>`; questo è un elemento di base, perciò avrà type `<class 'sqlparse.sql.Token'>`. In questo caso particolare, essendo un semplice spazio, sarà vero questo:

```py
pql_stat.tokens[1].is_whitespace # True
```

Prendiamo un elemento più complesso, come `<class 'sqlparse.sql.Identifier'>` che introduce un identificatore di tabella a WITH. Questo sarà di tipo `<class 'sqlparse.sql.Identifier'>`. In questo caso, il seguente flag indica che l'oggetto può essere ulteriormente esplorato: 

```py
pql_stat.tokens[4].is_whitespace # False
pql_stat.tokens[4].is_group # True
```

Su questo si potrà chiamare `.tokens` per ottenere ulteriori informazioni sullo statement. 


### Pulizia dei token dai newlines

Gli spazi non servono a molto. Per pulire dai newlines, 

```py
stat = [x for x in pql_stat.tokens if not x.is_whitespace]
```


### Come il parser codifica l'SQL

Clausola WITH:

- `<CTE 'WITH' at 0x2E283521940>`
  - identficatore di tabella: `<Identifier 'tab AS...' at 0x2E283538190>`
  - poi la SELECT
  - alla fine della SELECT parte un altro idenificatore di tabella
  - la clausola viene interrotta da un SELECT per l'intero WITH e da una punctation per la fine della singola subtable
    - punctation *virgola*: `<Punctuation ',' at 0x1F8757A2100>`
    - select statement: `<DML 'SELECT' at 0x1D0A3770D00>`

Clausola SELECT: 

- SELECT: `<DML 'SELECT' at 0x1D0A3770D00>`
  - `<IdentifierList 't2.col...' at 0x2E28353AA50>`

Struttura della clausola FROM:

- FROM: `<Keyword 'FROM' at 0x1D0A377D580>`
  - first tab: `<Identifier 'sch_ra...' at 0x1D0A3777C80>`
  - JOIN: `<Keyword 'LEFT J...' at 0x1D0A377D940>`
    - second tab: `<Identifier 'sch_ra...' at 0x1D0A3777DD0>`
    - `<Keyword 'ON' at 0x1D0A377DD00>`
    - `<Parenthesis '( fn.c...' at 0x2E28352C510>, <Punctuation ',' at 0x2E28352FFA0>`
    - **VEDI DIFETTO 1**: l'oggetto parenthesis tende a mangiarsi il WHERE a volte

Nota che in caso di subquery, la codifica diventa piuttosto involuta. L'oggetto subquery viene codificato per intero come un `<Identifier '(SELEC...' at 0x24AF4C01580>` che riporta lo statement `(SELECT DISTINCT * FROM tab) tab`. Accdendo nello statement, l'identificatore viene codificato come oggetto 

Struttura del where: 

- `<Where 'WHERE ...' at 0x1F875795E40>,`
  - richiamando `.tokens` viene fatta la scomposizione diretta
  - eventuali subqueries sono codificate con `<Parenthesis '(SELEC...' at 0x1DF80936740>` e non assorbono altri statement come succedeva per il DIFETTO 1. 

Struttura di group e having: 

- raggruppamento: `<Keyword 'GROUP ...' at 0x1F8757A61C0>`
  - seguito dagli identificatori del raggruppamento, raggruppati in un unico oggetto `<IdentifierList 'dim,dim' at 0x253D993F660>`
- selezione post raggruppamento: `<Keyword 'HAVING' at 0x253D9937B80>` a cui segue la scomposizione degli elementi
  - `<Function 'SUM(kp...' at 0x253D9926F90>`
  - `<Keyword 'BETWEEN' at 0x253D9937E20>`
  - `<Integer '50' at 0x253D9937EE0>`
  - `<Keyword 'AND' at 0x253D9937FA0>`
  - `<Integer '5000' at 0x253D99390A0>`

Order by e having:

- sorting: `<Keyword 'ORDER ...' at 0x253D9939160>`
  - seguito dagli identificatori, `<IdentifierList 'kpi_fi...' at 0x253D993F7B0>`
  - anche ci fosse una formula, raggrupperebbe lo stesso: `<IdentifierList 'NVL(kp...' at 0x26077D60970>`
- limit: `<Keyword 'LIMIT' at 0x26077D597C0>`
  - seguito da quanti elementi prendere: `<Integer '1' at 0x26077D59880>`

Commenti:

???


### DIFETTO 1 - la where

La clausola WHERE certe volte viene posta all'interno degli oggeti della JOIN, violando un po' la semantica del parsing. Questa può essere una bella complicazione. 

E' un difetto di struttura che spunta sol oquando c'è la keyword ON, quindi in quel caso penso basti solo andare a correggere l'algoritmo estraendo la WHERE da dove dovrebbe essere. 


### DIFETTO 2 - semantica del parsing un po' casuale

*Non è esattamente un difetto*, quanto piuttosto

Ci sono pochi metodi per capire che oggetto stiamo maneggiando, e parecchi elementi di disturbo. Il parser ha delle belle idee, ma l'albero sintattico che genera non è esattamente pulito. 

Alcune volte il parser riesce ad identificare bene gli idenifierList, mentre altre volte lascia tutto scomposto. Come ad esempio nel caso del GROUP BY che raggruppa, e HAVING che non raggruppa in questo modo. 




## Un algoritmo per modellare una query complessa

Una certa colonna passa attraverso diversi *layers*. Il layer più esterno è la root della query. Una query che non ha WITH statements *non è detto che sia priva di layers* perchè ci possono essere sempre delle subqueries. 

Un layer può essere:

- la query più esterna
- una subquery definita nel FROM
- una subquery definita nel WITH

diciamo che c'è una lista di layers, in ordine inverso. Vediamo la colonna sul risultato finale, e facciamo il salmone per arrivare al livello più basso. 


### La query più semplice del mondo 

Come nelle migliori tradizioni si parte dall'esempio elementare e si va rendendo l'algoritmo sempre più avanzato. Partiamo con questa qui: 

```sql
SELECT 
a,b,c
FROM tab1
```

In questo caso la query è composta da *un solo layer*. Desiderata: 

- chi sono le sorgenti della query? 
- chi sono le colonne? 
- che formula hanno le colonne? 
- a che layer vengono generale le colonne? 

Tutte queste informazioni possono essere ottenute direttamente scorrendo la query col parser.

Codice Py:

```py
def tokens(token_source):
    return [x for x in token_source if not x.is_whitespace]

sql = '...'
pql = tokens(sqlparse.parse(sql)[0])
print(pql)
for idx, item in enumerate(pql):
    print(f"[{idx}] =====")
    print(pql[idx])
```

Che ritorna come output in questo caso, 

```txt
[<DML 'SELECT' at 0x1DD585328E0>, 
<IdentifierList 'a,b,c' at 0x1DD5853B3C0>, 
<Keyword 'FROM' at 0x1DD58532C40>, 
<Identifier 'tab1' at 0x1DD5853B350>]
[0] =====
SELECT
[1] =====
a,b,c
[2] =====
FROM
[3] =====
tab1
```

Quindi, l'algoritmo dovrebbe essere:

- FOREACH elemento all'interno della lista di token
  - se SELECT
    - prendo l'elemento successivo, che sarà l'identifier list
    - FOREACH token nell'identifier list
      - traggo la colonna
      - traggo il nome della colonna come ulimo identificatore
      - traggo la formula dell'identificatore
  - se FROM
    - traggo la sorgente
    - assegno la sorgente a tutti gli oggetti trovati nella SELECT
  - 

Pensiamo anche alla struttura che può sintetizzare queste informazioni. 

```py
{
    'layers' : [
        'root'
    ],
    'columns' : {
        'a' : {
            'source_layer' : 0,
            'formula' : ''
        },
        'b' : {
            'source_layer' : 0,
            'formula' : ''
        },
        'c' : {
            'source_layer' : 0,
            'formula' : ''
        }
    },
    'where' : '',
    'from' : {
        'tab1' : {
            'source_layer' : 0
            'sources_count' : 0,
            'subquery' : '',
        }
    }
}
```

*Layers* : serve comunque mantenere un indice dei layers trovati durante il percorso. 


### leggermente meglio 

Aggiungiamo qualche formula e qualche statement di più. 

```sql
SELECT 
nvl(tab.a, tab.c) column_a, 
,tab.b AS column_b
,tab.c
FROM tab1 AS tab
ORDER BY 2,1,3
;
```

Quali sono i cambiamenti rispetto a prima:

- ORDER BY aggiunto, facile da gestire
- una formula
- la prima colonna non ha un AS come renaming
- la seconda colonna è un renaming con AS 
- la terza colonna non ha un renaming
- il FROM ha un alias

La rappresentazione raw cambia così:

```txt
============ PARSER RAW ============
[<DML 'SELECT' at 0x128A2B73B80>, <IdentifierList 'nvl(ta...' at 0x128A2B76900>, <Keyword 'FROM' at 0x128A2B807C0>, <Identifier 'tab1 A...' at 0x128A2B76740>, <Keyword 'ORDER ...' at 0x128A2B80AC0>, <IdentifierList '2,1,3' at 0x128A2B766D0>, <Punctuation ';' at 0x128A2B80DC0>]
[0] =====
SELECT
type: <class 'sqlparse.sql.Token'>
[1] =====
nvl(tab.a, tab.c) column_a,
tab.b AS column_b
,tab.c
type: <class 'sqlparse.sql.IdentifierList'>
[2] =====
FROM
type: <class 'sqlparse.sql.Token'>
[3] =====
tab1 AS tab
type: <class 'sqlparse.sql.Identifier'>
[4] =====
ORDER BY
type: <class 'sqlparse.sql.Token'>
[5] =====
2,1,3
type: <class 'sqlparse.sql.IdentifierList'>
[6] =====
;
type: <class 'sqlparse.sql.Token'>
============ PARSER RAW ============
```

L'order by, ai fini della ricerca del lineage, non ha alcuna importanza. Può essere ignorato. 

Per il caso del FROM bisogna fare un parsing accurato, perchè eslodendo quel FROM viene fuori questo :

```txt
tab1 <class 'sqlparse.sql.Token'>
AS <class 'sqlparse.sql.Token'>
tab <class 'sqlparse.sql.Identifier'>
```
Quindi purtroppo non una lista di token, ma tre token separati. E' uno dei difetti di questa libreria...

Per il FROM ci possono essere numerose casistiche:

- FROM tab
- FROM tab alias
- FROM tab AS alias

In quale di queste tre casistiche siamo? Occorre determinarlo. Però, nota bene che questi tre oggetti si trovano sotto una loro lista alla fin fine, 


### Inseriamo la GROUP BY

Un esempio con una group by e una having:

```sql
SELECT
COALESCE(col_a, '') AS col_a_new,
col_c,
ROUND(SUM(col_b),2) AS sum_col_b
FROM tab1 tab 
GROUP BY col_c, col_a
HAVING SUM(col_b) > 3/4 AND AVG(col_b) < 3
ORDER BY 2,1
```

La parte delle formule dovrebbe continuare a funzionare esattamente come prima. Anche la parte del FROM mi aspetto che funga a dovere. Mi aspetto anche che non ci sia nulla che possa dare info sugli altri campi mancanti. 

Per questa query, il parser ritorna una struttura di questo genere:

```txt
[<DML 'SELECT' at 0x23BB54A05E0>, <IdentifierList 'COALES...' at 0x23BB54B5C10>, <Keyword 'FROM' at 0x23BB54B2220>, <Identifier 'tab1 t...' at 0x23BB54B57B0>, <Keyword 'GROUP ...' at 0x23BB54B24C0>, <IdentifierList 'col_c,...' at 0x23BB54B5CF0>, <Keyword 'HAVING' at 0x23BB54B2760>, <Comparison 'SUM(co...' at 0x23BB54B59E0>, <Keyword 'AND' at 0x23BB54B2C40>, <Comparison 'AVG(co...' at 0x23BB54B5A50>, <Keyword 'ORDER ...' at 0x23BB54B30A0>, <IdentifierList '2,1' at 0x23BB54B5D60>]
[0] =====
SELECT
type: <class 'sqlparse.sql.Token'>
[1] =====
COALESCE(col_a, '') AS col_a_new,
col_c,
ROUND(SUM(col_b),2) AS sum_col_b
type: <class 'sqlparse.sql.IdentifierList'>
[2] =====
FROM
type: <class 'sqlparse.sql.Token'>
[3] =====
tab1 tab
type: <class 'sqlparse.sql.Identifier'>
[4] =====
GROUP BY
type: <class 'sqlparse.sql.Token'>
[5] =====
col_c, col_a
type: <class 'sqlparse.sql.IdentifierList'>
[6] =====
HAVING
type: <class 'sqlparse.sql.Token'>
[7] =====
SUM(col_b) > 3/4
type: <class 'sqlparse.sql.Comparison'>
[8] =====
AND
type: <class 'sqlparse.sql.Token'>
[9] =====
AVG(col_b) < 3
type: <class 'sqlparse.sql.Comparison'>
[10] =====
ORDER BY
type: <class 'sqlparse.sql.Token'>
[11] =====
2,1
type: <class 'sqlparse.sql.IdentifierList'>
```



### NEXT STEPS 

- l'obiettivo è quello di creare un dizionario dei nomi
  - nome della variaible
  - formula della variabile
  - condizione WHERE della variabile
  - condizione GROUP BY della variabile
  - condizione HAVING della variabile
  - il layer in cui è generata la variabile
  - *il passaggio che porta le variabili ad avere delle dipendenze è un passaggio ulteriore*
- inserire le JOIN
- inserire le subqueries



### Mapping delle formule

L'obiettivo è creare, a partire dallo statement SQL, un dizionario che contenga tutti i nomi delle variabili disponibili all'interno della tabella. Ogni variabile ha un certo numero di formule associate, da cui deriva in prima istanza:

- formula select
- formula where
- "formula" from
  - è il nome della tabella e le varie JOIN
  - in caso di subqueries, la formula è la subquery direttamente
- formula group
- formula having

Analizzando il contenuto della formula, sono in grado di riconoscere le quantità da cui essa proviene. Ogni quantità che trovo, la aggiungo al dizionario. Per ogni colonna in particolare voglio sapere:

- identificatore tabella.colonna
  - usato come chiave del dictionary
- il layer in cui viene considerata la quantità
  - table (sempre root) o una subtable (nome assegnato in automatico) o una WITH (nome assegnato da query)
  - per l'identificazione del layer si procede ad una scomposizione della query per step da esplorare
- identificatori tabella.colonna da cui discende
  - una lista di identificatori
- le formule che concorrono alla sua creazione
  - select
  - from
  - where
  - grou by
  - having
  - qualify

In altre parole, dato uno statement SQL, voglio poterlo scomporre in tante queries separate, una per colonna. 

Partiamo dal caso semplice, e arriviamo al caso complesso. Dal più semplice possibile: 

```txt
Formula SELECT:
col1
[<Identifier 'col1' at 0x225D2E052E0>]
<class 'sqlparse.sql.Identifier'>
è un gruppo? True
Esplodo l'oggetto, dato che è un gruppo:
[<Name 'col1' at 0x225D2E03940>]
<class 'sqlparse.sql.Token'>
source della formula:
col1
```

Questo è il caso semplice. Nelle query in cui un campo viene chiamato secco dalla tabella sorgente. In questo caso, aggiungo un solo elemento alla lista: col1, dopo aver identificato la tabella da cui discende. Supponiamo sia *tab1*, 

```py
cols_dict = {
  'col1' : {
    'layer' : 'root
    'sources' : [
      'tab1.col1'
    ],
    'select_formula' : {
      'formula' : '',
      'sources' : [ ]
    },
    'from_formula' : [
      {
        'formula' : 'FROM tab1',
        'sources' : [ 'tab1' ]
      }
    ]
    'where_formula' : {},
    'groupby_formula' : {},
    'having_formula' : {},
    'qualify_formula' : {}
  }
}
```

E' importante qui sottolineare che da parte dell'algoritmo occorre avere un modo, data la formula, di ottenere tutte le colonne necessarie per il suo calcolo. 

Un caso simile ma leggermente più complesso:

```txt
Formula SELECT:
tab1.col1
[<Identifier 'tab1.c...' at 0x2A5B68943C0>]
E' un identifier, caso 1; esplodo l'identifier
[<Name 'tab1' at 0x2A5B6892940>, <Punctuation '.' at 0x2A5B68929A0>, <Name 'col1' at 0x2A5B6892A00>]
Posso riconoscere una DOT notation direttamente guardando la lista di tipi
["<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>"]
source della formula: tab1.col1
```

In questo caso la struttura che descrive questa formula diventa:

```py
cols_dict = {
  'tab1.col1' : {
    'layer' : 'root
    'sources' : [
      'tab1.col1'
    ],
    'select_formula' : {
      'formula' : 'tab1.col1',
      'sources' : [ 'tab1.col1' ]
    },
    'from_formula' : [
      {
        'formula' : 'FROM tab1',
        'sources' : [ 'tab1' ]
      }
    ]
    'where_formula' : {},
    'groupby_formula' : {},
    'having_formula' : {},
    'qualify_formula' : {}
  }
}
```

Passiamo ad un caso con renaming:

```txt
Formula SELECT:
col1 AS column_alias
[<Identifier 'col1 A...' at 0x26DDE9155F0>]
esplodo l'oggetto
[<Name 'col1' at 0x26DDE914CA0>, <Whitespace ' ' at 0x26DDE914C40>, <Keyword 'AS' at 0x26DDE914D00>, <Whitespace ' ' at 0x26DDE914D60>, <Identifier 'column...' at 0x26DDE915660>]
soddisfa la dot notation? False
soddisfa la single column notation? False
l'oggetto non soddisfa i due passi base, quindi scatta la normalizzazione
Nome della variabile: column_alias
Post normalizzazione:
[<Name 'col1' at 0x26DDE914CA0>]
REITERO l'algoritmo su quello che rimane. In questo caso, ho direttamente l'oggetto Token
soddisfa la dot notation? False
soddisfa la single column notation? True
source della formula: col1
```

Il risultato atteso diventerà dunque il seguente:

```py
cols_dict = {
  'column_alias' : {
    'layer' : 'root
    'sources' : [
      'tab1.col1'
    ],
    'select_formula' : {
      'formula' : 'col1',
      'sources' : [ 'col1' ]
    },
    'from_formula' : [
      {
        'formula' : 'FROM tab1',
        'sources' : [ 'tab1' ]
      }
    ]
    'where_formula' : {},
    'groupby_formula' : {},
    'having_formula' : {},
    'qualify_formula' : {}
  }
}
```

Mischiamo un attimo le carte: 

```txt
Formula SELECT:
tab.b AS column_b
[<Identifier 'tab.b ...' at 0x2718FDE4F90>]
esplodo l'identifier
[<Name 'tab' at 0x2718FDF2CA0>, <Punctuation '.' at 0x2718FDF2C40>, <Name 'b' at 0x2718FDF2D00>, <Whitespace ' ' at 0x2718FDF2D60>, <Keyword 'AS' at 0x2718FDF2DC0>, <Whitespace ' ' at 0x2718FDF2E20>, <Identifier 'column...' at 0x2718FDE4F20>]
soddisfa la dot notation? False
soddisfa la single column notation? True
Non soddisfa entrambe le condizioni, quindi procedi alla SPLIT
FOUND IDENTIFIER: column_b
la sua formula è
[<Name 'tab' at 0x2718FDF2CA0>, <Punctuation '.' at 0x2718FDF2C40>, <Name 'b' at 0x2718FDF2D00>]
REITERO esplodo l'identifier
[<Name 'tab' at 0x2718FDF2CA0>, <Punctuation '.' at 0x2718FDF2C40>, <Name 'b' at 0x2718FDF2D00>]
soddisfa la dot notation? True
soddisfa la single column notation? False
Soddisfa la DOT notation! Source --> tab.b
```

Comlichiamo un attimino le cose, aggiungendo una semplice operazione. 

```txt
Formula SELECT:
tab.a + b AS value_vl
[<Identifier 'tab.a ...' at 0x228F650BB30>]

>>> WRAPPER: esplodo e verifico
[<Operation 'tab.a ...' at 0x228F650BAC0>, <Whitespace ' ' at 0x228F6508B20>, <Keyword 'AS' at 0x228F6508B80>, <Whitespace ' ' at 0x228F6508BE0>, <Identifier 'value_...' at 0x228F650BA50>]
soddisfa la dot notation? False
soddisfa la single column notation? False
soddisfa la operation? False
Non soddisfa nessuna delle tre, quindi splitto e itero perchè ci sarà sicuramente un AS; è proprio per gestire questa casistica che esiste il wrapper dell'algoritmo.
alias--> value_vl

>>> ITERAZIONE 0: eplodo e verifico
[<Operation 'tab.a ...' at 0x228F650BAC0>]
soddisfa la dot notation? False
soddisfa la single column notation? False
soddisfa la operation? True
è una operation! Itero su questa

>>> ITERAZIONE 1: eplodo e verifico
[<Identifier 'tab.a' at 0x228F650B970>, <Whitespace ' ' at 0x228F65089A0>, <Operator '+' at 0x228F6508A00>, <Whitespace ' ' at 0x228F6508A60>, <Identifier 'b' at 0x228F650B9E0>]
soddisfa la dot notation? False
soddisfa la single column notation? False
soddisfa la operation? False
Nessuna delle tre condizioni è soddisfatta, quindi passo a smazzare elemento per elemento
FOREACH item IN tokens_list
[0] è un identifier? True --> REITERO ed esplodo il caso --> is dot? True
[1] è un identifier? False
[2] è un identifier? False
[3] è un identifier? False
[4] è un identifier? True --> REITERO ed esplodo il caso --> is col? True
```

E se avessi un'operazione composta? Potrebbe comparire l'oggetto parenthesis. 





### Rule per l'interpretazione delle formule

*Il primo step è sicuramente quello di estrarre il contenuto grezzo della query.cUn avolta fatto quello, posso concentrarmi sull'interpretazione delle varie formule.*

*L'algoritmo di interpretazione della formula va strutturato come un wrapper più una funzione che effettivamente puù iterare.*

Per la ricerca delle variabili occorre impostare un algoritmo ricorsivo. L'oggetto iniziale può essere:

- `[<Identifier 'col1' at 0x20EC3B14270>]` nei casi
  - singola colonna (passo elementare) o colonna in dot notation, PASSO BASE
  - formula + alias, in cui la formula può essere anche una funzione; ricorda qui in ogni caso di usare la normalizzazione della formula, SERVE WRAPPARE
- `<Operation 'tab.a ...' at 0x15BD8E18AC0>` nei casi di operazione algebrica tra quantità secche o funzioni, uno dei casi su cui iterare, SERVE ITERARE

Passo base: se mi viene dato un identificatore, lo esplodo. Se mi viene dato all'inizio altro, allora ci lavoro direttamente. Lo riconosco dal type: usa `str(type(tk)) == "<class 'sqlparse.sql.Identifier'>"` per riconoscere un identifier. **NON PASSARE UNA LISTA ALL'ALGORITMO SE INTENDI PASSARE UN OGGETTO DA ESPLODERE:** se gli passi una lista, allora significa che l'oggetto è già esploso. 

- `col1`: la source è col1, rinominata tab.col1 a segito dell'interpretazione del FROM
  - lo ottengo come oggetto `<Identifier 'col1' at 0x225D2E052E0>`
  - esplodo l'oggetto
  - e trovo un elemento solo di tipo `<class 'sqlparse.sql.Token'>`
  - estraggo il token diretto
- `tab.col1`: la source è tab.col1
  - lo ottengo come oggetto `[<Identifier 'tab1.c...' at 0x225D2E053C0>]`
  - esplodo l'oggetto
  - e trovo tre elementi di tipo `["<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>", "<class 'sqlparse.sql.Token'>"]` di cui quello centrale è un `<Punctuation '.' at 0x225D2E03A00>` e di cui gli altri due sono `<Name 'col1' at 0x225D2E03A60>`
  - estraggo elemento tre DOT elemento 1

In caso di renaming, 

- normalizzazione
  - cerca tutto quello che precede l'AS
  - il nome della variabile è quello che segue l'AS, proprio in fondo
  - la formula è tutto quel che precede l'AS escluso eventuale spazio bianco alla fine
- split della formula in un alias e una parte di formula
  - aggungi al dict il nome che hai trovato
  - e esplora la formula



## Riguardo l'interpretazione della FROM

Assumiamo anzitutto che la query sia corretta, quindi non ci sono ambiguità sui nomi. Laddove non è possibile dire solo guardando la query da dove discenda una certa colonna, è comunqe possibile ottenere un'estrazione dalla tabella sorgente se nota, e individuare univocamente quel campo in una certa tabella. 

parlo in particolare del caso delle JOIN in cui non viene usata la dot notation perchè si da per scontato che un campo provenga da una una certa tabella. 