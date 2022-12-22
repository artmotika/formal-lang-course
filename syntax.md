# Описание синтаксиса языка запросов к графам

## Описание абстрактного синтаксиса языка
```
prog = List<stmt>

stmt =
    bind of var * expr
  | print of expr

val =
    String of string
  | Int of int
  | Bool of bool
  | Regex of string // Регулярное выражение
  | Cfg of string   // КС-грамматика

expr =
    Var of var                    // переменные
  | Val of val                    // константы
  | Set_start of expr * expr      // задать множество стартовых состояний
  | Set_final of expr * expr      // задать множество финальных состояний
  | Add_start of expr * expr      // добавить состояния в множество стартовых
  | Add_final of expr * expr      // добавить состояния в множество финальных
  | Get_start of expr             // получить множество стартовых состояний
  | Get_final of expr             // получить множество финальных состояний
  | Get_reachable of expr         // получить все пары достижимых вершин
  | Get_vertices of expr          // получить все вершины
  | Get_edges of expr             // получить все рёбра
  | Get_labels of expr            // получить все метки
  | Map of lambda * expr          // классический map
  | Filter of lambda * expr       // классический filter
  | Load of path                  // загрузка графа
  | Intersect of expr * expr      // пересечение языков
  | Concat of expr * expr         // конкатенация языков
  | Union of expr * expr          // объединение языков
  | Star of expr                  // замыкание языков (звезда Клини)
  | Contains of expr * expr       // проверка на вхождение элемента в множество
  | Set of List<expr>             // множество элементов

lambda =
    Lambda of pattern * expr

pattern ->
    Var
  | expr * expr * expr  // ребро
  | pair                // пара

pair ->
    pair * pair
  | expr * expr

```

## Описание конкретного синтаксиса языка
```
prog ->
   stmt ';' prog
  | eps

stmt ->
    var '=' expr
  | 'print' '(' expr ')'

val ->
    int
  | str
  | bool
  | regex
  | cfg

int -> '0' | '-'? [1-9][0-9]*
bool ->
    'true'
  | 'false'
str -> '"' ( _ | . | [a-z] | [A-Z] ) ( _ | . | [a-z] | [A-Z] | [0-9] | \n )* '"'
regex -> 'r' str
cfg -> 'c' str

expr ->
    var
  | val
  | 'set_starts' '(' expr ',' expr ')'       // graph expr
  | 'set_finals' '(' expr ',' expr ')'       // graph expr
  | 'add_starts' '(' expr ',' expr ')'       // graph expr
  | 'add_finals' '(' expr ',' expr ')'       // graph expr
  | 'get_starts' '(' expr ')'                // graph expr
  | 'get_finals' '(' expr ')'                // graph expr
  | 'get_reachable' '(' expr ')'             // graph expr
  | 'get_vertices' '(' expr ')'              // graph expr
  | 'get_edges' '(' expr ')'                 // graph expr
  | 'get_labels' '(' expr ')'                // graph expr
  | 'map' '(' lambda ',' expr ')'
  | 'filter' '(' lambda ',' expr ')'
  | 'load' '(' path ')'                      // graph expr
  | expr '&' expr                            // intersection
  | expr '^' expr                            // concatenation
  | expr '|' expr                            // union
  | 'star' '(' expr ')'                      // Kleene star
  | expr 'in' expr                           // contains
  | '{' (expr (',' expr)*)? '}'              // set
  | '(' expr ')'                             // вложенное выражение

var -> str
path -> '"' ( / | _ | . | [a-z] | [A-Z] | [0-9] )+ '"'

lambda -> 'lambda' pattern '->' expr

pattern ->
    var
  | edge
  | pair

edge -> '(' expr ',' expr ',' expr ')'

pair ->
    '(' pair ',' pair ')'
  | '(' expr ',' expr ')'

```

## Примеры
### Множество достижимых вершин из определенного множества вершин
```
g = load("graph1.dot");

reachable_pairs = filter(lambda (a, _) -> (a in {3, 5, 6}), get_reachable(g));
res = map(lambda (_, b) -> (b), reachable_pairs);
print(res);

g = set_starts({3, 5, 6}, g);
res = map(lambda (_, b) -> (b), get_reachable(g));
print(res);
```

### Множество пар вершин удовлетворяющих регулярному выражению
```
g1 = load("graph1.dot");
regex = r"georges|(Det.N)";

res = map(lambda ((a, b), (_, _)) -> (a, b), get_reachable(g1 & regex));
print(res);
```

### Множество пар вершин удовлетворяющих КС-грамматике
```
g1 = load("graph1.dot");
cfg = c"S -> a S b | a b";

res = map(lambda ((a, b), (_, _)) -> (a, b), get_reachable(g1 & cfg));
print(res);
```
