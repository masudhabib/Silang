import unittest
import lexer


class TestBASIC(unittest.TestCase):
    def test_define_string(self):
        result = lexer.lexer.lex('define foo is "bar"')
        token_list = list(result)
        print(token_list)
        self.assertEqual("DEFINE", token_list[0].name)
        self.assertEqual("IDENTIFIER", token_list[1].name)
        self.assertEqual("IS", token_list[2].name)
        self.assertEqual("STRING", token_list[3].name)

    def test_define_number(self):
        result = lexer.lexer.lex('define foo is 0')
        token_list = list(result)
        self.assertEqual("DEFINE", token_list[0].name)
        self.assertEqual("IDENTIFIER", token_list[1].name)
        self.assertEqual("IS", token_list[2].name)
        self.assertEqual("INTEGER", token_list[3].name)

    def test_add(self):
        result = lexer.lexer.lex('1 + 1')
        token_list = list(result)
        self.assertEqual("INTEGER", token_list[0].name)
        self.assertEqual("PLUS", token_list[1].name)
        self.assertEqual("INTEGER", token_list[2].name)

    def test_sub(self):
        result = lexer.lexer.lex('2 - 1')
        token_list = list(result)
        self.assertEqual("INTEGER", token_list[0].name)
        self.assertEqual("MINUS", token_list[1].name)
        self.assertEqual("INTEGER", token_list[2].name)

    def test_mul(self):
        result = lexer.lexer.lex('2 * 1')
        token_list = list(result)
        self.assertEqual("INTEGER", token_list[0].name)
        self.assertEqual("MUL", token_list[1].name)
        self.assertEqual("INTEGER", token_list[2].name)

    def test_div(self):
        result = lexer.lexer.lex('2 / 1')
        token_list = list(result)
        self.assertEqual("INTEGER", token_list[0].name)
        self.assertEqual("DIV", token_list[1].name)
        self.assertEqual("INTEGER", token_list[2].name)


class TestList(unittest.TestCase):
    def test_list(self):
        result = lexer.lexer.lex('[5]')
        token_list = list(result)
        self.assertEqual("[", token_list[0].name)
        self.assertEqual("INTEGER", token_list[1].name)
        self.assertEqual("]", token_list[2].name)

        result = lexer.lexer.lex('[5,]')
        token_list = list(result)
        self.assertEqual("[", token_list[0].name)
        self.assertEqual("INTEGER", token_list[1].name)
        self.assertEqual(",", token_list[2].name)
        self.assertEqual("]", token_list[3].name)

        result = lexer.lexer.lex('[5, 6]')
        token_list = list(result)
        self.assertEqual("[", token_list[0].name)
        self.assertEqual("INTEGER", token_list[1].name)
        self.assertEqual(",", token_list[2].name)
        self.assertEqual("INTEGER", token_list[3].name)
        self.assertEqual("]", token_list[4].name)


class TestFunctions(unittest.TestCase):
    def test_addition(self):
        result = lexer.lexer.lex('increase(foo)')
        token_list = list(result)
        self.assertEqual("INCREASE", token_list[0].name)
        self.assertEqual("(", token_list[1].name)
        self.assertEqual("IDENTIFIER", token_list[2].name)
        self.assertEqual(")", token_list[3].name)

    def test_print(self):
        result = lexer.lexer.lex('print("foo")')
        token_list = list(result)
        self.assertEqual("PRINT", token_list[0].name)
        self.assertEqual("(", token_list[1].name)
        self.assertEqual("STRING", token_list[2].name)
        self.assertEqual(")", token_list[3].name)


class TestIF(unittest.TestCase):
    def test_if_else(self):
        result = lexer.lexer.lex('if true: true else: false end')
        token_list = list(result)
        self.assertEqual("IF", token_list[0].name)
        self.assertEqual("BOOLEAN", token_list[1].name)
        self.assertEqual("COLON", token_list[2].name)
        self.assertEqual("BOOLEAN", token_list[3].name)
        self.assertEqual("ELSE", token_list[4].name)
        self.assertEqual("COLON", token_list[5].name)
        self.assertEqual("END", token_list[7].name)


class TestWHILE(unittest.TestCase):
    def test_while(self):
        code = "while a != 3: end"
        result = lexer.lexer.lex(code)
        token_list = list(result)
        self.assertEqual("WHILE", token_list[0].name)
        self.assertEqual("IDENTIFIER", token_list[1].name)
        self.assertEqual("!=", token_list[2].name)
        self.assertEqual("INTEGER", token_list[3].name)
        self.assertEqual("COLON", token_list[4].name)
        self.assertEqual("END", token_list[5].name)


class TestFOR(unittest.TestCase):
    def test_for(self):
        code = "for b in [1]: end"
        result = lexer.lexer.lex(code)
        token_list = list(result)
        self.assertEqual("FOR", token_list[0].name)
        self.assertEqual("IDENTIFIER", token_list[1].name)
        self.assertEqual("IN", token_list[2].name)
        self.assertEqual("[", token_list[3].name)
        self.assertEqual("INTEGER", token_list[4].name)
        self.assertEqual("]", token_list[5].name)
        self.assertEqual("COLON", token_list[6].name)
        self.assertEqual("END", token_list[7].name)


if __name__ == '__main__':
    unittest.main()