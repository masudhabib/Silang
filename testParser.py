import unittest
import parser


class TestEnvironment(object):
    def __init__(self):
        self.variables = {}


class TestBASIC(unittest.TestCase):
    def setUp(self):
        self.state_ = parser.ParserState()
        self.env_ = TestEnvironment()

    def test_define_string(self):
        result = parser.parse('define a is "Hello"', self.state_).evaluate(self.env_)
        self.assertEqual('Hello', result.to_string())

    def test_define_number(self):
        result = parser.parse('define b is 55', self.state_).evaluate(self.env_)
        self.assertEqual(str(result), "55")

    def test_add(self):
        result = parser.parse('2 + 1', self.state_).evaluate(self.env_)
        self.assertEqual(result.to_string(), '3')

    def test_sub(self):
        result = parser.parse('2 - 1', self.state_).evaluate(self.env_)
        self.assertEqual(result.to_string(), '1')

    def test_mul(self):
        result = parser.parse('2 * 3', self.state_).evaluate(self.env_)
        self.assertEqual(result.to_string(), '6')

    def test_div(self):
        result = parser.parse('6 / 3', self.state_).evaluate(self.env_)
        self.assertEqual(result.to_string(), '2')


class TestList(unittest.TestCase):
    def setUp(self):
        self.s = parser.ParserState()
        self.e = TestEnvironment()

    def test_list(self):
        result = parser.parse('[1]', self.s).evaluate(self.e)
        self.assertEqual(result.to_string(), '[1]')

        result = parser.parse('define b is [1,]', self.s).evaluate(self.e)
        self.assertEqual(result.to_string(), '[1]')

        result = parser.parse('[1,2]', self.s).evaluate(self.e)
        self.assertEqual(result.to_string(), '[1, 2]')


class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.state_ = parser.ParserState()
        self.env_ = TestEnvironment()

    def test_addition(self):
        result = parser.parse('define a is 10', self.state_).evaluate(self.env_)
        self.assertEqual('10', str(result))

        parser.parse('increase(a)', self.state_).evaluate(self.env_)
        parser.parse('increase(a)', self.state_).evaluate(self.env_)
        result = parser.parse('a == 12', self.state_).evaluate(self.env_)
        self.assertEqual('true', result.to_string())

    def test_print(self):
        result = parser.parse('print("Hello")', self.state_).evaluate(self.env_)
        self.assertEqual(result, 'Hello')

        result = parser.parse('define a is "Hello"', self.state_).evaluate(self.env_)
        self.assertEqual(result.to_string(), 'Hello')

        result = parser.parse('print(a)', self.state_).evaluate(self.env_)
        self.assertEqual(result, 'Hello')


class TestIF(unittest.TestCase):
    def setUp(self):
        self.state_ = parser.ParserState()
        self.env_ = TestEnvironment()

    def test_if(self):
        result = parser.parse('if true: true end', self.state_).evaluate(self.env_)
        self.assertEqual(result.to_string(), 'true')

        result = parser.parse('if false: true end', self.state_).evaluate(self.env_)
        self.assertEqual(type(result), parser.Null)

    def test_if_else(self):
        result = parser.parse('1 == 2', self.state_).evaluate(self.env_)
        self.assertEqual(result.to_string(), 'false')

        result = parser.parse('if true: true else: false end', self.state_).evaluate(self.env_)
        self.assertEqual(result.to_string(), 'true')


class TestWHILE(unittest.TestCase):
    def setUp(self):
        self.state_ = parser.ParserState()
        self.env_ = TestEnvironment()

    def test_while(self):
        result = parser.parse('define a is 0', self.state_).evaluate(self.env_)
        self.assertEqual(str(result), "0")

        code = "while a != 3:" \
               "increase(a)" \
               "end"
        result = parser.parse(code, self.state_).evaluate(self.env_)
        self.assertEqual('3', '3')


class TestFOR(unittest.TestCase):
    def setUp(self):
        self.state_ = parser.ParserState()
        self.env_ = TestEnvironment()

    def test_for_print(self):
        code = "for b in [1, 2, 3, 4]:" \
               "print(b)" \
               "end"
        result = parser.parse(code, self.state_).evaluate(self.env_)
        self.assertEqual('Print', 'Print')

    def test_for_add(self):
        result = parser.parse('define a is 0', self.state_).evaluate(self.env_)
        self.assertEqual(str(result), "0")

        code = "for i in [1, 2]:" \
               "define a is i + 1" \
               "end"
        result = parser.parse(code, self.state_).evaluate(self.env_)

        result = parser.parse('print(a)', self.state_).evaluate(self.env_)
        self.assertEqual(result, "3")


if __name__ == '__main__':
    unittest.main()








