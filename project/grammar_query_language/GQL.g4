grammar GQL;

prog: (WS* stmt SEMI WS*)+ EOF ;

stmt:
    ID EQUALS expr
    | print PARL expr PARR ;

val:
    INT
    | STR
    | bool
    | REGEX
    | CFG ;

bool: 'true' | 'false' ;

expr:
    ID
  | val
  | SET_STARTS PARL expr COMMA expr PARR       // graph expr
  | SET_FINALS PARL expr COMMA expr PARR       // graph expr
  | ADD_STARTS PARL expr COMMA expr PARR       // graph expr
  | ADD_FINALS PARL expr COMMA expr PARR       // graph expr
  | GET_STARTS PARL expr PARR                  // graph expr
  | GET_FINALS PARL expr PARR                  // graph expr
  | GET_REACHABLE PARL expr PARR               // graph expr
  | GET_VERTICIES PARL expr PARR               // graph expr
  | GET_EDGES PARL expr PARR                   // graph expr
  | GET_LABELS PARL expr PARR                  // graph expr
  | MAP PARL lambda COMMA expr PARR
  | FILTER PARL lambda COMMA expr PARR
  | LOAD PARL STR PARR                         // graph expr
  | expr INTERSECT expr                        // intersection
  | expr CONCAT expr                           // concatenation
  | expr UNITE expr                            // union
  | STAR PARL expr PARR                        // Kleene star
  | expr CONTAINS expr                         // contains
  | CURLYL (expr (COMMA expr)*)? CURLYR        // set
  | PARL expr PARR ;                           // вложенное выражение

lambda: LAMBDA pattern ARROW (pattern | expr);

pattern:
    ID
    | edge
    | pair ;

edge: PARL expr COMMA expr COMMA expr PARR ;

pair:
    PARL pair COMMA pair PARR
    | PARL expr COMMA expr PARR ;

LAMBDA: 'lambda' ;
ARROW: '->' ;

SET_STARTS: 'set_starts' ;
SET_FINALS: 'set_finals' ;
ADD_STARTS: 'add_starts' ;
ADD_FINALS: 'add_finals' ;
GET_STARTS: 'get_starts' ;
GET_FINALS: 'get_finals' ;
GET_REACHABLE: 'get_reachable' ;
GET_VERTICIES: 'get_vertices' ;
GET_EDGES: 'get_edges' ;
GET_LABELS: 'get_labels' ;
MAP: 'map' ;
FILTER: 'filter' ;
LOAD: 'load' ;
INTERSECT: '&' ;
CONCAT: '^' ;
UNITE: '|' ;
STAR: 'star' ;
CONTAINS: 'in' ;
CURLYL: '{' ;
CURLYR: '}' ;
PARL: '(' ;
PARR: ')' ;

ID : [_a-zA-Z] [_a-zA-Z0-9]* ;
BOOL : 'true' | 'false' ;
INT : '0' | '-'? [1-9][0-9]* ;
STR : '"' .*? '"' ;
REGEX : 'r' STR ;
CFG : 'c' STR ;

print : 'print' ;
EQUALS : '=' ;
COMMA: ',' ;
SEMI : ';' ;
WS : [ \r\t\n]+ -> skip ; // skip spaces, tabs, newlines
