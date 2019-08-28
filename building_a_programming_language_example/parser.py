from rply import ParserGenerator
from building_a_programming_language_example.ast import Number, Sum, Sub, Print


class Parser:
    def __init__(self, module, builder, printf):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            [
                'PRINT', 'OPEN_PAREN', 'CLOSE_PAREN', 'OPEN_BRACE',
                'CLOSE_BRACE', 'OPEN_BLOCK', 'CLOSE_BLOCK', 'SEMI_COLON',
                'COLON', 'SUM', 'SUB', 'MUL', 'DIV', 'POW', 'NUMBER', 'TEXT',
                'TIMESERIES', 'STEADY_STATE', 'DOSE_RESPONSE', 'OSCILLATIONS',
                'TRANSIENT', 'HYPERBOLIC', 'SIGMOIDAL', 'UP', 'DOWN', 'MEAN',
                'MAX', 'MIN', 'ALL', 'ANY', 'TIME', 'COMMA', 'NEWLINE',
                'FOUR_SPACES', 'GT', 'LT', 'GE', 'LE', 'EQ', 'NEQ', 'ASSIGNMENT' ],
            [
                ('left', ['TEXT']),
                ('left', ['PLUS', 'MINUS']),
                ('left', ['MUL', 'DIV']),
                ('left', ['POW']),
                ('left', ['OPEN_PAREN', 'CLOSE_PAREN']),
                ('left', ['ALL', 'ANY', 'MEAN', 'MIN', 'MAX']),
                ('left', ['TIMESERIES', 'STEADY_STATE', 'DOSE_RESPONSE']),
            ]
        )
        self.module = module
        self.builder = builder
        self.printf = printf

    def parse(self):
        @self.pg.production('statement : expression')
        def statement_expr(state, p):
            return p[0]

        @self.pg.production('statement : LET IDENTIFIER = expression')
        def statement_assignment(state, p):
            return Assignment(Variable(p[1].getstr()), p[3])

    #     @self.pg.production('program : PRINT OPEN_PAREN expression CLOSE_PAREN SEMI_COLON')
    #     def program(p):
    #         return Print(self.builder, self.module, self.printf, p[2])
    #
    #     @self.pg.production('expression : expression SUM expression')
    #     @self.pg.production('expression : expression SUB expression')
    #     def expression(p):
    #         left = p[0]
    #         right = p[2]
    #         operator = p[1]
    #         if operator.gettokentype() == 'SUM':
    #             return Sum(self.builder, self.module, left, right)
    #         elif operator.gettokentype() == 'SUB':
    #             return Sub(self.builder, self.module, left, right)
    #
    #     @self.pg.production('expression : NUMBER')
    #     def number(p):
    #         return Number(self.builder, self.module, p[0].value)
    #
    #     @self.pg.error
    #     def error_handle(token):
    #         raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
