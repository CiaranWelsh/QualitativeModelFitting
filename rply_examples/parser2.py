# from rply import ParserGenerator
from building_a_programming_language_example.ast import Number, Sum, Sub, Print
from lark import Lark



l = Lark('''
start: WORD "," WORD "!"
%import common.WORD
%ignore " "            
''')

print(l.parse('Hello, World!'))














