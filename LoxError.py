import sys

class LoxException(Exception):
    def __init__(self, token, message):
        """Initializes a LoxException
        object for errors.
        >>> from Token import Token
        >>> error = LoxException(Token('COMMA', 1, ',', None), "some error")
        >>> error.message
        'some error'
        >>> error.token
        Token('COMMA', 1, ',', None)
        """
        self.message = message
        self.token = token

def error(token, message, end):
    """Displays error for
    user to handle.
    >>> from Token import Token
    >>> error(Token('COMMA', 1, ',', None), "some error message", True)
    [line 1] Error at end: some error message.
    LoxException(Token('COMMA', 1, ',', None), 'some error message')
    >>> error(Token('COMMA', 1, ',', None), "some error message", False)
    [line 1] Error at ',': some error message.
    LoxException(Token('COMMA', 1, ',', None), 'some error message')
    """
    if end == True:
        print(f"[line {token.get_line()}] Error at end: {message}.")
    else:
        print(f"[line {token.get_line()}] Error at \'{token.get_lexeme()}\': {message}.")
    return LoxException(token, message)

def runtime_error(error):
    """Handles runtime errors
    and displays them. (Tested manually)
    """
    print(f"{error.message}\n[line {error.token.get_line()}]")
    sys.exit(70)

if __name__ == '__main__':
    import doctest
    doctest.testmod()