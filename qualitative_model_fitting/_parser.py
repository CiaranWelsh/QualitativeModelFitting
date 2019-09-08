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
    // clause1                 : [FUNC] (model_entity | expression)
    // clause2                 : [FUNC] (model_entity | expression)

    
    expression              : term+
                            //| model_entity
    //                        | NUMBER NUMERICAL_OPERATOR NUMBER 
    //                        | NUMBER                            
    //                        | model_entity NUMERICAL_OPERATOR NUMBER 
    //                        | NUMBER NUMERICAL_OPERATOR model_entity 
                            
    ?term                   : addop
                            | mulop
                            | NUMBER
    
    
    addop.2                 : term ADD term -> add 
                            | term SUB term -> sub
    
    
    mulop                   : term MUL term -> mul
                            | term DIV term -> div
                                
                            // NUMBER "**" NUMBER -> pow
                            // | NUMBER "*" NUMBER -> mul
                            // | NUMBER "/" NUMBER -> div
                            // | NUMBER "+" NUMBER -> plus
                            // | NUMBER "-" NUMBER -> minus
                            //| numerical_expression NUMERICAL_OPERATOR numerical_expression
    
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
    ADD                     : "+"
    SUB                     : "-"
    MUL                     : "*"
    DIV                     : "/"
    POW                     : "**"
    NUMERICAL_OPERATOR      : ADD
                            | SUB
                            | MUL
                            | DIV
                            | POW
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
