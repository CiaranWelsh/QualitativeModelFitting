import unittest

from rply_examples.lexer import Lexer
from rply_examples.parser import Parser

class LexerTests(unittest.TestCase):

    def setUp(self) -> None:
        self.string1 = """
        timeseries InsulinOnly{
            Insulin=1
        }
        IRS1a[InsulinOnly]@t=20 > IRS1a[InsulinOnly]@t=0;
        
        """

    def test(self):
        l = Lexer().get_lexer()
        tokens = l.lex(self.string1)
        count = 0
        for i in tokens:
            count += 1
        actual = count
        expected = 21
        self.assertEqual(expected, actual)


class testtest(unittest.TestCase):

    def setUp(self) -> None:
        self.x = "x = 4"

    def test(self):
        l = Lexer().get_lexer().lex(self.x)
        p = Parser().parse()

if __name__ == '__main__':
    unittest.main()
