class LogicError(Exception):
    def __str__(self):
        return "Logic error!"


class UnexpectedEndError(Exception):
    def __str__(self):
        return "Unexpected end of code!"


class UnexpectedTokenError(Exception):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return f"Unexpected token: {self.token}!"

class LexingError(Exception):
    def __str__(self):
        return 'Lexing Error!'


