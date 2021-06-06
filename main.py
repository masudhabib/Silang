import sys
import lexer
import parser
from errors import *


# For Pycharm: press the green button in the gutter to run the command-line interface.
if __name__ == '__main__':
    state_ = parser.ParserState()
    while True:
        # Start point
        text_input = input('Silang code:\n')

        try:
            result = parser.parse(text_input, state_).evaluate(state_)
            parser.print_parse_result(result)
        except UnexpectedEndError as e:
            print(e)
            continue
        except UnexpectedTokenError as e:
            print(f"Unexpected token error: {e}.")
            continue
        except LogicError as e:
            print(e)
            continue