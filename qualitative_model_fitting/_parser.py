from lark import Lark


# todo implement combinations modifier

class Parser:
    grammar = """
    start                   : block+
    block                   : _timeseries_block  
                            | observation_block 
    _timeseries_block        : "timeseries" SYMBOL "{" ts_arg_list "}" START "," STOP "," STEP
    ts_arg_list             : (ts_arg [","])*
    ts_arg                  : SYMBOL "=" FLOAT 
                            | SYMBOL "=" DIGIT+
                            
    
    observation_block       : "observation" statement+
    statement               : OBS_NAME ":" clause1 OPERATOR clause2
    name                    : 
    OPERATOR                : ">" 
                            | "<" 
                            | "==" 
                            | "!="
                            | "<="
                            | ">="
    clause1                 : [FUNC] model_entity
                            
    clause2                 : [FUNC] model_entity
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
    
    %import common.DIGIT
    %import common.NUMBER
    %import common.FLOAT
    %import common.WORD
    %import common.LETTER
    %import common.WS
    %ignore WS
    """

    def __init__(self):
        self.lark = Lark(self.grammar)

    def parse(self, string):
        return self.lark.parse(string)

    def pretty(self, string):
        return self.lark.parse(string).pretty()
