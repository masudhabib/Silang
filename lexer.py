from rply import LexerGenerator
import re

lg = LexerGenerator()

# type
lg.add('INTEGER', '-?\d+')
lg.add('STRING', '(""".*?""")|(".*?")|(\'.*?\')')
lg.add('BOOLEAN', "true(?!\w)|false(?!\w)")
lg.add('IS', "is(?!\w)")

# logic
lg.add('IF', 'if(?!\w)')
lg.add('ELSE', 'else(?!\w)')
lg.add('END', 'end(?!\w)')
lg.add('DEFINE', 'define(?!\w)')
lg.add('FOR', 'for(?!\w)')
lg.add('ITEM', 'item(?!\w)')
lg.add('IN', 'in(?!\w)')
lg.add('WHILE', 'while(?!\w)')
lg.add('RETURN', 'return(?!\w)')
lg.add('COLON', ':')
lg.add('(', '\(')
lg.add(')', '\)')

# function
lg.add('PRINT', 'print(?!\w)')
lg.add('INCREASE', 'increase(?!\w)')

lg.add('IDENTIFIER', "[a-zA-Z_][a-zA-Z0-9_]*")
lg.add('PLUS', '\+')
lg.add('MINUS', '-')
lg.add('MUL', '\*')
lg.add('DIV', '/')
lg.add('==', '==')
lg.add('!=', '!=')

# list
lg.add('[', '\[')
lg.add(']', '\]')
lg.add(',', ',')

# remove whitespace
lg.ignore('[ \t\r\f\v]+')

lexer = lg.build()


def lex(source):
    lines = r'([\s]+)(?:\n)'

    line = re.search(lines, source)
    while line is not None:
        start, end = line.span(1)
        assert start >= 0 and end >= 0
        line = re.search(lines, source)

    return lexer.lex(source)
