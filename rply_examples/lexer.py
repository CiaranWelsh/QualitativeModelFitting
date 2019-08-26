from rply import LexerGenerator



class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Print
        self.lexer.add('PRINT', r'print')
        # Parenthesis
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')
        self.lexer.add('OPEN_BRACE', r'\{')
        self.lexer.add('CLOSE_BRACE', r'\}')
        self.lexer.add('OPEN_BLOCK', r'\[')
        self.lexer.add('CLOSE_BLOCK', r'\]')
        # Semi Colon
        self.lexer.add('SEMI_COLON', r'\;')
        self.lexer.add('COLON', r'\:')
        # Operators
        self.lexer.add('SUM', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'\\')
        self.lexer.add('POW', r'\*\*')
        # Number
        self.lexer.add('NUMBER', r'\d+')
        # text
        self.lexer.add('TEXT', r'\w+')
        # Ignore spaces
        self.lexer.ignore('\s+')
        # time series condition (replaces the 'condition' idea since all are types of condition)
        self.lexer.add('TIMESERIES', r'timeseries')
        self.lexer.add('STEADY_STATE', r'steady_state')
        self.lexer.add('DOSE_RESPONSE', r'dose_response')
        # behavioural types
        self.lexer.add('OSCILLATIONS', r'oscillations')
        self.lexer.add('TRANSIENT', r'transient')
        self.lexer.add('HYPERBOLIC', r'hyperbolic')
        self.lexer.add('SIGMOIDAL', r'sigmoidal')
        # directional modifiers
        self.lexer.add('UP', r'up')
        self.lexer.add('DOWN', r'down')
        #function modifiers
        self.lexer.add('MEAN', 'mean')
        self.lexer.add('MAX', 'max')
        self.lexer.add('MIN', 'min')
        self.lexer.add('ALL', 'all')
        self.lexer.add('ANY', 'any')
        # time
        self.lexer.add('TIME', '@t=')
        # punctuation
        self.lexer.add('COMMA', ',')
        self.lexer.add('NEWLINE', '\n')
        self.lexer.add('FOUR_SPACES', '    ')
        # comparison operators
        self.lexer.add('GT', '>')
        self.lexer.add('LT', '<')
        self.lexer.add('GE', '>=')
        self.lexer.add('LE', '<=')
        self.lexer.add('EQ', '==')
        self.lexer.add('NEQ', '!=')
        self.lexer.add('ASSIGNMENT', '=')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()

































