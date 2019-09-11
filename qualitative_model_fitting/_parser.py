from lark import Lark, Transformer, v_args, Visitor

from ._simulator import TimeSeries

# todo implement combinations modifier

class Parser:
    grammar = """
    start                  : block+
    ?block                  : timeseries_block  
                            | steadystate_block
                            | observation_block 
    timeseries_block        : "timeseries" NAME "{" ts_arg_list "}" START "," STOP "," STEP
    steadystate_block       : "steadystate" NAME "{" ts_arg_list "}" 
    ?ts_arg_list            : (ts_arg [","])*
    ?ts_arg                 : NAME "=" FLOAT 
                            | NAME "=" DIGIT+
                            
    
    observation_block       : "observation" statement+
    ?statement              : comparison_statement | behavioural_statement
    comparison_statement    : OBS_NAME ":" clause1 OPERATOR clause2
    behavioural_statement   : OBS_NAME ":" qual_exp 
    clause1                 : [function] expression
    clause2                 : [function] expression
    
    ?expression             : term ((ADD|SUB) term)*
    ?term                   : factor ((MUL
                                      |DIV 
                                      |MOD
                                      |FLOOR) factor)*
    ?factor                 : ("+"|"-") factor 
                            | atom
                            | power
    ?power                  : atom "**" factor
    ?atom                   : NUMBER 
                            | NAME
                            | model_entity
    
    ?model_entity           : NAME "[" CONDITION "]" [_TIME_SYMBOL (POINT_TIME| INTERVAL_TIME)] 
    ?function               : FUNC
    ?qual_exp                : SHAPE [DIRECTION] model_entity
    
    SHAPE                   : "hyperbolic"
                            | "transient"
                            | "sigmoidal"
                            | "oscillation"
    DIRECTION               : "up" 
                            | "down"
    
    OPERATOR                : ">"
                            | "<" 
                            | "==" 
                            | "!="
                            | "<="
                            | ">="
    FUNC                    : "mean"|"all"|"any"|"min"|"max"
    _TIME_SYMBOL            : "@t=" 
    POINT_TIME              :  DIGIT+
    INTERVAL_TIME           : "(" DIGIT+ [WS]* "," [WS]* DIGIT + ")"
    OBS_NAME                : NAME
    CONDITION               : NAME
    NAME                    : /(?!\d+)[A-Za-z0-9]+/
    START                   : DIGIT+
    STOP                    : DIGIT+
    STEP                    : DIGIT+
    POW                     : "**"
    MUL                     : "*"
    DIV                     : "/"
    ADD                     : "+"
    SUB                     : "-"
    MOD                     : "%"
    FLOOR                   : "//"
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
