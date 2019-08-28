from rply import ParserGenerator
from building_a_programming_language_example.ast import Number, Sum, Sub, Print


class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            [
                'PRINT', 'OPEN_PAREN', 'CLOSE_PAREN', 'OPEN_BRACE',
                'CLOSE_BRACE', 'OPEN_BLOCK', 'CLOSE_BLOCK', 'SEMI_COLON',
                'COLON', 'SUM', 'SUB', 'MUL', 'DIV', 'POW', 'NUMBER', 'TEXT',
                'TIMESERIES', 'STEADY_STATE', 'DOSE_RESPONSE', 'OSCILLATIONS',
                'TRANSIENT', 'HYPERBOLIC', 'SIGMOIDAL', 'UP', 'DOWN', 'MEAN',
                'MAX', 'MIN', 'ALL', 'ANY', 'TIME', 'COMMA', 'NEWLINE',
                'FOUR_SPACES', 'GT', 'LT', 'GE', 'LE', 'EQ', 'NEQ', 'ASSIGNMENT'],
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

    def parse(self):
        @self.pg.production('')
        def assign(p):
            return Assignment(p)

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()