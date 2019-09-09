from lark import Lark, Transformer, v_args, Visitor

from ._simulator import TimeSeries

# todo implement combinations modifier

class Parser:
    grammar = """
    start                   : block+
    block                   : timeseries_block  
                            | observation_block 
    timeseries_block        : "timeseries" SYMBOL "{" ts_arg_list "}" START "," STOP "," STEP
    ts_arg_list             : (ts_arg [","])*
    ts_arg                  : SYMBOL "=" FLOAT 
                            | SYMBOL "=" DIGIT+
                            
    
    observation_block       : "observation" statement+
    statement               : OBS_NAME ":" clause1 OPERATOR clause2
    OPERATOR                : ">" 
                            | "<" 
                            | "==" 
                            | "!="
                            | "<="
                            | ">="
    clause1                 : [FUNC] expression
    clause2                 : [FUNC] expression

    ?expression             : term ((ADD|SUB) term)*
    ?term.2                 : factor ((MUL|DIV) factor)*
    ?factor                 : NUMBER | model_entity 
    
    model_entity            : SYMBOL "[" CONDITION "]" _TIME_SYMBOL (POINT_TIME| INTERVAL_TIME) 
    FUNC                    : "mean"|"all"|"any"|"min"|"max"
    _TIME_SYMBOL            : "@t=" 
    POINT_TIME              :  DIGIT+
    INTERVAL_TIME           : "(" DIGIT+ [WS]* "," [WS]* DIGIT + ")"
    SYMBOL                  : /[A-Za-z0-9]+/
    OBS_NAME                : SYMBOL
    CONDITION               : SYMBOL
    START                   : DIGIT+
    STOP                    : DIGIT+
    STEP                    : DIGIT+
    POW                     : "**"
    MUL                     : "*"
    DIV                     : "/"
    ADD                     : "+"
    SUB                     : "-"
    NUMERICAL_OPERATOR      : "+"
                            | "-"
                            | "*"
                            | "/"
                            | "**"
                            | "//"
                            | "%"
    COMMENT                 : /\/\/.*/
    %import common.DIGIT
    %import common.NUMBER
    %import common.FLOAT
    %import common.WORD
    %import common.LETTER
    %import common.WS
    %ignore WS
    %ignore COMMENT
    """

    def __init__(self):
        self.lark = Lark(self.grammar)

    def parse(self, string):
        return self.lark.parse(string)

    def pretty(self, string):
        return self.lark.parse(string).pretty()
