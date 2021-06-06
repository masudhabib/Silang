from rply import ParserGenerator
from ast import *
from errors import *
import lexer


# state instance which gets passed to parser to store all declared variables
class ParserState(object):
    def __init__(self):
        self.variables = {}


pg = ParserGenerator(
    # A list of all token names, accepted by the parser.
    ['STRING', 'INTEGER', 'IDENTIFIER', 'BOOLEAN',
     'PLUS', 'MINUS', 'MUL', 'DIV',
     'IF', 'ELSE', 'COLON', 'END', 'DEFINE', 'WHILE', 'FOR', 'IN', 'PRINT', 'INCREASE',
     '(', ')', 'IS', '==', '!=', '[', ']', ',',
     '$end',
     ],
    # A list of precedence rules with ascending precedence, to
    # disambiguate ambiguous production rules.
    precedence=[
        ('left', ['DEFINE', ]),
        ('left', ['IS']),
        ('left', ['[', ']', ',']),
        ('left', ['IF', 'COLON', 'ELSE', 'END', 'WHILE', 'FOR', 'IN', 'ITEM', 'PRINT', 'INCREASE']),
        ('left', ['==', '!=']),
        ('left', ['PLUS', 'MINUS', ]),
        ('left', ['MUL', 'DIV', ]),

    ]
)

# =================================code block=================================
@pg.production("main : program")
def main_program(self, p):
    # p is a list of the pieces matched by the right hand side of the
    # rule
    return p[0]


@pg.production('program : statement_full')
def program_statement(state, p):
    return Program(p[0])


@pg.production('statement_full : statement $end')
def statement_full(state, p):
    return p[0]


@pg.production('statement : expression')
def statement_expr(state, p):
    return p[0]


# =================================basic=================================
@pg.production('statement : DEFINE IDENTIFIER IS expression')
def statement_assignment(state, p):
    return Assignment(Variable(p[1].getstr()), p[3])


@pg.production('const : BOOLEAN')
def expression_boolean(state, p):
    return Boolean(True if p[0].getstr() == 'true' else False)


@pg.production('const : INTEGER')
def expression_integer(state, p):
    return Integer(int(p[0].getstr()))


@pg.production('const : STRING')
def expression_string(state, p):
    return String(p[0].getstr().strip('"\''))


@pg.production('expression : const')
def expression_const(state, p):
    return p[0]


@pg.production('expression : expression PLUS expression')
@pg.production('expression : expression MINUS expression')
@pg.production('expression : expression MUL expression')
@pg.production('expression : expression DIV expression')
def expression_binop(state, p):
    left = p[0]
    right = p[2]

    if p[1].gettokentype() == 'PLUS':
        return Add(left, right)
    elif p[1].gettokentype() == 'MINUS':
        return Sub(left, right)
    elif p[1].gettokentype() == 'MUL':
        return Mul(left, right)
    elif p[1].gettokentype() == 'DIV':
        return Div(left, right)
    else:
        raise LogicError('Arithmetic operations error!')


@pg.production('expression : expression != expression')
@pg.production('expression : expression == expression')
def expression_equality(state, p):
    left = p[0]
    right = p[2]
    check = p[1]

    if check.gettokentype() == '==':
        return Equal(left, right)
    elif check.gettokentype() == '!=':
        return NotEqual(left, right)
    else:
        raise LogicError("Shouldn't be possible")


@pg.production('expression : IDENTIFIER')
def expression_variable(state, p):
    return Variable(p[0].getstr())


# =================================list=================================
@pg.production('expression : [ expression ]')
def expression_list_single(state, p):
    return List(p[1])


@pg.production('expression : [ expressionlist ]')
def expression_list(state, p):
    return p[1]


@pg.production('expression : expression [ expression ]')
def expression_list_index(state, p):
    return Index(p[0], p[2])


@pg.production('expressionlist : expression , expressionlist')
def arglist(state, p):
    # expressionlist is a List
    p[2].push(p[0])
    return p[2]


@pg.production('expressionlist : expression')
@pg.production('expressionlist : expression ,')
def expressionlist_single(state, p):
    a = List(p[0])
    return a


# =================================if else=================================
@pg.production('expression : IF expression COLON statement END')
def expression_if_single_line(state, p):
    return If(condition=p[1], body=p[3])


@pg.production('expression : IF expression COLON statement ELSE COLON statement END')
def expression_if_else_single_line(state, p):
    return If(condition=p[1], body=p[3], else_body=p[6])


# =================================while loop=================================
@pg.production('expression : WHILE expression COLON statement END')
def expression_while(state, p):
    return While(condition=p[1], body=p[3])


# =================================for loop=================================
@pg.production('expression : FOR IDENTIFIER IN expression COLON statement END')
def expression_for(state, p):
    return For(item=Variable(p[1].getstr()), sequence=p[3], body=p[5])


# =================================functions=================================
@pg.production('expression : ( expression )')
def expression_parens(state, p):
    return p[1]


@pg.production('expression : PRINT ( expression )')
def expression_print(state, p):
    return Print(p[2])


@pg.production('expression : INCREASE ( IDENTIFIER )')
def expression_addition(state, p):
    left = p[2]
    return Addition(Variable(left.getstr()))


# =================================error handling=================================
@pg.error
def error_handler(state, token):
    print(token)
    pos = token.getsourcepos()
    if pos:
        raise UnexpectedTokenError(token.gettokentype())
    elif token.gettokentype() == '$end':
        raise UnexpectedEndError()
    else:
        raise UnexpectedTokenError(token.gettokentype())


parser = pg.build()
state = ParserState()

def print_parse_result(result):
    if hasattr(result, 'to_string'):
        print(result.to_string())
    else:
        print(str(result))


def parse(code, state=state):
    result = parser.parse(lexer.lexer.lex(code), state)
    return result
