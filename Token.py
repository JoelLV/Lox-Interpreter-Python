class Token:
    def __init__(self, token_type, line, lexeme = None, literal = None):
        """Initializes a token object.
        >>> obj = Token("COMMA", 1, ",")
        >>> obj.TOKEN_TYPE
        'COMMA'
        >>> obj.LINE
        1
        >>> obj.LITERAL
        >>> obj.LEXEME
        ','
        >>> obj = Token("DOT", 10, '.', "Something")
        >>> obj.TOKEN_TYPE
        'DOT'
        >>> obj.LINE
        10
        >>> obj.LITERAL
        'Something'
        >>> obj.LEXEME
        '.'
        """
        self.TOKEN_TYPE = token_type
        self.LINE = line
        self.LITERAL = literal
        self.LEXEME = lexeme
    
    def __str__(self):
        """Returns a human-readable
        string representing a Token object
        >>> obj = Token("COMMA", 1)
        >>> str(obj)
        "Type: 'COMMA', Line: 1, Literal: None"
        >>> obj = Token("DOT", 11, literal = ".")
        >>> str(obj)
        "Type: 'DOT', Line: 11, Literal: '.'"
        """
        return f"Type: {self.TOKEN_TYPE!r}, Line: {self.LINE!r}, Literal: {self.LITERAL!r}"
    
    def __repr__(self):
        """Returns a python-executable
        string representing a Token object
        >>> obj = Token("COMMA", 1, ',', None)
        >>> repr(obj)
        "Token('COMMA', 1, ',', None)"
        >>> obj = Token("STRING", 10, literal = "Something")
        >>> repr(obj)
        "Token('STRING', 10, None, 'Something')"
        >>> obj = Token("AND", 2, lexeme = "and")
        >>> repr(obj)
        "Token('AND', 2, 'and', None)"
        """
        return f"Token({self.TOKEN_TYPE!r}, {self.LINE!r}, {self.LEXEME!r}, {self.LITERAL!r})"
    
    def get_token_type(self):
        """Getter method for field
        self.TOKEN_TYPE
        """
        return self.TOKEN_TYPE
    
    def get_line(self):
        """Getter method for field
        self.LINE
        """
        return self.LINE
    
    def get_literal(self):
        """Getter method for field
        self.LITERAL
        """
        return self.LITERAL
    
    def get_lexeme(self):
        """Getter method for field
        self.LEXEME
        """
        return self.LEXEME

if __name__ == '__main__':
    import doctest
    doctest.testmod()