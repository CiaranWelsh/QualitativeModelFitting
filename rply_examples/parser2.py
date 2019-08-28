# from rply import ParserGenerator
from building_a_programming_language_example.ast import Number, Sum, Sub, Print
from lark import Lark


grammar = """
start           : statement
statement       : clause operator clause
operator        : ">"   -> gl
                | "<"   -> lt
                | "="   -> eq
                | "!="  -> neq
                | "<="  -> ge
                | ">="  -> le
clause          : SYMBOL "[" SYMBOL "]" _TIME_SYMBOL POINT_TIME 
                | SYMBOL "[" SYMBOL "]" _TIME_SYMBOL INTERVAL_TIME 
SYMBOL          : /[A-Za-z0-9]+/
_TIME_SYMBOL    : "@t=" 
POINT_TIME      :  DIGIT+
INTERVAL_TIME   : "@t=(" DIGIT+ "," DIGIT + ")"

%import common.DIGIT
%import common.WORD
%import common.LETTER
%import common.WS
%ignore WS
"""

tests = [
    "word > other",
    "IRS1a[condition]@t=10 > Akt[condition]@t=10"
]

l = Lark(grammar)

print(l.parse(tests[1]).pretty())














