from Token import Token

class Scanner:
    def __init__(self, source):
        """Initializes Scanner object
        >>> scnr = Scanner('')
        >>> scnr.source
        ''
        >>> scnr = Scanner(["var something = 100;", "var anotherThing = 10;"])
        >>> scnr.source
        ['var something = 100;', 'var anotherThing = 10;']
        """
        self.source = source
        self.lox_error = False
    
    def set_source(self, source):
        """Sets field self.source
        >>> scnr = Scanner('')
        >>> scnr.set_source(['something'])
        >>> scnr.source
        ['something']
        >>> scnr.set_source('')
        >>> scnr.source
        ''
        """
        self.source = source

    def get_tokens(self):
        """Searches each line provided by source
        for tokens. Returns a list with all
        tokens in source. The source is a list of lists containing strings
        representing lines of code.
        >>> scnr = Scanner(["var something = 100;", "var anotherThing = 10;"])
        >>> scnr.get_tokens()
        [Token('VAR', 1, 'var', None), Token('IDENTIFIER', 1, 'something', None), Token('EQUAL', 1, '=', None), Token('NUMBER', 1, '100', 100.0), Token('SEMICOLON', 1, ';', None), Token('VAR', 2, 'var', None), Token('IDENTIFIER', 2, 'anotherThing', None), Token('EQUAL', 2, '=', None), Token('NUMBER', 2, '10', 10.0), Token('SEMICOLON', 2, ';', None), Token('EOF', 2, None, None)]
        >>> scnr.source = ["", ""]
        >>> scnr.get_tokens()
        [Token('EOF', 2, None, None)]
        """
        try:
            all_token_list = []
            for i in range(len(self.source)):
                all_token_list.extend(self.get_tokens_in_line(self.source[i], i + 1))
            all_token_list.append(Token("EOF", len(self.source)))
            return all_token_list
        except Exception:
            return None

    def get_tokens_in_line(self, line, line_num):
        """Looks for tokens in line provided.
        Returns a list with tokens found in line.
        >>> scnr = Scanner("")
        >>> scnr.get_tokens_in_line('(){},.-+;*', 1)
        [Token('LEFT_PAREN', 1, '(', None), Token('RIGHT_PAREN', 1, ')', None), Token('LEFT_BRACE', 1, '{', None), Token('RIGHT_BRACE', 1, '}', None), Token('COMMA', 1, ',', None), Token('DOT', 1, '.', None), Token('MINUS', 1, '-', None), Token('PLUS', 1, '+', None), Token('SEMICOLON', 1, ';', None), Token('STAR', 1, '*', None)]
        >>> scnr.get_tokens_in_line('!= ! == = < <= > >=', 1)
        [Token('NOT_EQUAL', 1, '!=', None), Token('NOT', 1, '!', None), Token('EQUAL_EQUAL', 1, '==', None), Token('EQUAL', 1, '=', None), Token('LESS_THAN', 1, '<', None), Token('LESS_EQUAL', 1, '<=', None), Token('GREATER_THAN', 1, '>', None), Token('GREATER_EQUAL', 1, '>=', None)]
        >>> scnr.get_tokens_in_line('//Some comment that must be ignored', 10)
        []
        >>> scnr.get_tokens_in_line('/', 2)
        [Token('SLASH', 2, '/', None)]
        >>> scnr.get_tokens_in_line('\"Some string that needs to be stored\"', 2)
        [Token('STRING', 2, 'Some string that needs to be stored', 'Some string that needs to be stored')]
        >>> scnr.get_tokens_in_line('100 19', 3)
        [Token('NUMBER', 3, '100', 100.0), Token('NUMBER', 3, '19', 19.0)]
        >>> scnr.get_tokens_in_line('Variable something there', 1)
        [Token('IDENTIFIER', 1, 'Variable', None), Token('IDENTIFIER', 1, 'something', None), Token('IDENTIFIER', 1, 'there', None)]
        >>> scnr.get_tokens_in_line('and class else false for fun if nil or print return super this true var while', 1)
        [Token('AND', 1, 'and', None), Token('CLASS', 1, 'class', None), Token('ELSE', 1, 'else', None), Token('FALSE', 1, 'false', None), Token('FOR', 1, 'for', None), Token('FUN', 1, 'fun', None), Token('IF', 1, 'if', None), Token('NIL', 1, 'nil', None), Token('OR', 1, 'or', None), Token('PRINT', 1, 'print', None), Token('RETURN', 1, 'return', None), Token('SUPER', 1, 'super', None), Token('THIS', 1, 'this', None), Token('TRUE', 1, 'true', None), Token('VAR', 1, 'var', None), Token('WHILE', 1, 'while', None)]
        """
        token_list = []
        SINGLE_LEXEMES = {
            '(':"LEFT_PAREN",
            ')':"RIGHT_PAREN",
            '{':"LEFT_BRACE",
            '}':"RIGHT_BRACE",
            ',':"COMMA",
            '.':"DOT",
            '-':"MINUS",
            '+':"PLUS",
            ';':"SEMICOLON",
            '*':"STAR",
        }
        OPERATOR_LEXEMES = {
            '!=':"NOT_EQUAL",
            '!':"NOT",
            '==':"EQUAL_EQUAL",
            '=':"EQUAL",
            '<':"LESS_THAN",
            '<=':"LESS_EQUAL",
            '>':"GREATER_THAN",
            '>=':"GREATER_EQUAL"
        }
        IGNORE_CHARS = ' ', '\r', '\t', '\n', ''
        i = 0
        while i < len(line):
            if line[i] in SINGLE_LEXEMES:
                token_list.append(Token(SINGLE_LEXEMES[line[i]], line_num, lexeme = line[i]))
            elif line[i] in OPERATOR_LEXEMES:
                if (i < len(line) - 1) and line[i + 1] == '=':
                    token_list.append(Token(OPERATOR_LEXEMES[line[i] + '='], line_num, lexeme = line[i] + '='))
                    i += 1
                else:
                    token_list.append(Token(OPERATOR_LEXEMES[line[i]], line_num, lexeme = line[i]))
            elif line[i] == '/':
                if (i < len(line) - 1) and line[i + 1] == '/':
                    break
                else:
                    token_list.append(Token("SLASH", line_num, lexeme = line[i]))
            elif line[i] in IGNORE_CHARS:
                pass
            elif line[i] == '\"':
                end_index = self.get_end_index_for_strings(line, i)
                if end_index == -1:
                    print(f"[line {line_num}] Unterminated string.")
                    self.lox_error = True
                else:
                    literal = line[i + 1:end_index]
                    lexeme = str(literal)
                    token_list.append(Token("STRING", line_num, lexeme, literal))
                i = end_index
            else:
                if self.is_digit(line[i]):
                    end_index = self.get_end_index_for_numbers(line, i)
                    lexeme = str(int(line[i:end_index + 1]) if '.' not in str(line[i:end_index + 1]) else float(line[i:end_index + 1]))
                    literal = float(line[i:end_index + 1])
                    token_list.append(Token("NUMBER", line_num, lexeme, literal))
                    i = end_index
                elif line[i].isalpha():
                    token, end_index = self.get_token_for_identifiers(line, i, line_num)
                    token_list.append(token)
                    i = end_index
                else:
                    print(f"[line {line_num}] Unexpected character. {line[i]}")
                    self.lox_error = True
            i += 1
        
        return token_list

    def get_token_for_identifiers(self, line, start_index, line_number):
        """Determines whether the segment of the line scanned
        is an identifier or a reserved word, then it
        returns the token accordingly and the index
        where it stopped scanning.
        >>> scnr = Scanner("")
        >>> scnr.get_token_for_identifiers('var something more', 0, 3)
        (Token('VAR', 3, 'var', None), 2)
        >>> scnr.get_token_for_identifiers('var something more', 4, 2)
        (Token('IDENTIFIER', 2, 'something', None), 12)
        >>> scnr.get_token_for_identifiers('oregon', 0, 1)
        (Token('IDENTIFIER', 1, 'oregon', None), 5)
        >>> scnr.get_token_for_identifiers('oregon2', 0, 1)
        (Token('IDENTIFIER', 1, 'oregon2', None), 6)
        """
        RESERVED_WORDS = {
            "and":"AND",
            "class":"CLASS", 
            "else":"ELSE",
            "false":"FALSE", 
            "for":"FOR",
            "fun":"FUN", 
            "if":"IF",
            "nil":"NIL",
            "or":"OR", 
            "print":"PRINT",
            "return":"RETURN", 
            "super":"SUPER",
            "this":"THIS", 
            "true":"TRUE",
            "var":"VAR",
            "while":"WHILE"
        }
        i = start_index
        while i < len(line):
            if line[i].isalpha() or self.is_digit(line[i]):
                i += 1
                continue
            else:
                break
        identifier = line[start_index:i]
        if identifier in RESERVED_WORDS:
            return Token(RESERVED_WORDS[identifier], line_number, lexeme = identifier), i - 1
        else:
            return Token("IDENTIFIER", line_number, lexeme = identifier), i - 1

    def get_end_index_for_strings(self, line, start_index):
        """Returns the index of the second double
        quote character. If not found, the function
        returns -1.
        >>> scnr = Scanner('')
        >>> scnr.get_end_index_for_strings('\"Something else far\"', 0)
        19
        >>> scnr.get_end_index_for_strings('\"Something for my father', 0)
        -1
        """
        for index in range(start_index + 1, len(line)):
            if line[index] == '\"':
                return index
        else:
            return -1

    def get_end_index_for_numbers(self, line, start_index):
        """Returns the index where the last number
        is found in the line.
        >>> scnr = Scanner('')
        >>> scnr.get_end_index_for_numbers('for something 1029 there', 14)
        17
        >>> scnr.get_end_index_for_numbers('102945439543', 0)
        11
        """
        for index in range(start_index + 1, len(line)):
            if self.is_digit(line[index]):
                continue
            else:
                if index < len(line) - 1 and line[index] == '.' and self.is_digit(line[index + 1]):
                    continue
                else:
                    return index - 1
        return len(line) - 1

    def is_digit(self, char):
        """Determines if a character is a digit.
        >>> scnr = Scanner('')
        >>> scnr.is_digit('0')
        True
        >>> scnr.is_digit('g')
        False
        >>> scnr.is_digit('9')
        True
        >>> scnr.is_digit('5')
        True
        >>> scnr.is_digit('2')
        True
        >>> scnr.is_digit('7')
        True
        """
        return char >= '0' and char <= '9'

if __name__ == '__main__':
    import doctest
    doctest.testmod()