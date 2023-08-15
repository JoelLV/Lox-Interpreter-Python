from ExprSubClasses import Binary, Get, This, Unary, Literal, Grouping, Variable, Assign, Logical, Call, Set, Super
import LoxError
from StmtSubClasses import Print, Expression, Return, Var, Block, If, While, Function, Class

class Parser:
    def __init__(self, tokens):
        """Initializes Parser object
        >>> parser = Parser(None)
        >>> str(parser.tokens)
        'None'
        >>> str(parser.index)
        '0'
        """
        self.tokens = tokens
        self.index = 0
        self.lox_error = False

    def parse(self):
        """Parses the tokens
        in the field self.tokens
        """
        statements = []
        while self.tokens[self.index].get_token_type() != 'EOF':
            statements.append(self.declaration())

        return statements
    
    def declaration(self):
        """Representation of declaration
        as a grammar rule.
        """
        try:
            if self.is_equal('VAR'):
                return self.var_declaration()
            elif self.is_equal('FUN'):
                return self.function("function")
            elif self.is_equal('CLASS'):
                return self.class_declaration()
            else:
                return self.statement()
        except LoxError.LoxException:
            self.synchronize()
            return None

    def class_declaration(self):
        """Representation of
        class declaration as a grammar
        rule.
        """
        name = self.consume('IDENTIFIER', "Expect class name")

        superclass = None
        if self.is_equal('LESS_THAN'):
            self.consume('IDENTIFIER', "Expect superclass name")
            superclass = Variable(self.tokens[self.index - 1])

        self.consume('LEFT_BRACE', "Expect \'{\' before class body")

        methods = []
        while self.tokens[self.index].get_token_type() != 'RIGHT_BRACE' and self.tokens[self.index].get_token_type != 'EOF':
            methods.append(self.function("method"))
        
        self.consume('RIGHT_BRACE', "Expect \'}\' after class body")

        return Class(name, superclass, methods)

    def var_declaration(self):
        """Representation of
        var declaration as a grammar
        rule.
        """
        name = self.consume('IDENTIFIER', "Expect variable name")
        initializer = None

        if self.is_equal('EQUAL'):
            initializer = self.expression()
        
        self.consume('SEMICOLON', "Expect \';\' after variable declaration")
        return Var(name, initializer)

    def function(self, kind):
        """Representation of
        a function declaration as a
        grammar rule.
        """
        name = self.consume('IDENTIFIER', f"Expect {kind} name")
        self.consume('LEFT_PAREN', f"Expect \'(\' after {kind} name")
        parameters = []
        if self.tokens[self.index].get_token_type() != 'RIGHT_PAREN':
            while True:
                if len(parameters) >= 255:
                    self.error(self.tokens[self.index], "Can\'t have more than 255 parameters")
                
                parameters.append(self.consume('IDENTIFIER', "Expect parameter name"))

                if not self.is_equal('COMMA'):
                    break
        self.consume('RIGHT_PAREN', "Expect \')\' after parameters")

        self.consume('LEFT_BRACE', "Expect \'{\' before " + kind + " body")
        body = self.block()
        return Function(name, parameters, body)

    def statement(self):
        """Representation of statement
        as a grammar rule.
        """
        if self.is_equal('PRINT'):
            return self.print_statement()
        elif self.is_equal('LEFT_BRACE'):
            return Block(self.block())
        elif self.is_equal('IF'):
            return self.if_statement()
        elif self.is_equal('WHILE'):
            return self.while_statement()
        elif self.is_equal('FOR'):
            return self.for_statement()
        elif self.is_equal('RETURN'):
            return self.return_statement()
        else:
            return self.expression_statement()
    
    def print_statement(self):
        """Representation of print
        statement as a grammar rule.
        """
        value = self.expression()
        self.consume('SEMICOLON', "Expect \';\' after value")

        return Print(value)
    
    def if_statement(self):
        """Representation of an if
        statement as a grammar rule.
        """
        self.consume('LEFT_PAREN', "Expect \'(\' after \'if\'")
        condition = self.expression()
        self.consume('RIGHT_PAREN', "Expect \')\' after if condition")

        then_branch = self.statement()
        else_branch = None

        if self.is_equal('ELSE'):
            else_branch = self.statement()
        
        return If(condition, then_branch, else_branch)
    
    def while_statement(self):
        """Representation of a while loop
        statement as a grammar rule.
        """
        self.consume('LEFT_PAREN', "Expect \'(\' after \'while\'")
        condition = self.expression()
        self.consume('RIGHT_PAREN', "Expect \')\' after condition")
        body = self.statement()

        return While(condition, body)
    
    def for_statement(self):
        """Representation of a for loop
        statement as a grammar rule.
        """
        self.consume('LEFT_PAREN', "Expect \'(\' after \'for\'")

        initializer = None
        if self.is_equal('SEMICOLON'):
            initializer = None
        elif self.is_equal('VAR'):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()
        
        condition = None
        if self.tokens[self.index].get_token_type() != 'EOF' and self.tokens[self.index].get_token_type() != 'SEMICOLON':
            condition = self.expression()
        self.consume('SEMICOLON', "Expect \';\' after loop condition")
    
        increment = None
        if self.tokens[self.index].get_token_type() != 'EOF' and self.tokens[self.index].get_token_type() != 'RIGHT_PAREN':
            increment = self.expression()
        self.consume('RIGHT_PAREN', "Expect \')\' after for clauses")

        body = self.statement()

        if increment != None:
            body = Block([body, Expression(increment)])
        
        if condition == None:
            condition = Literal(True)
        body = While(condition, body)

        if initializer != None:
            body = Block([initializer, body])

        return body

    def block(self):
        """Representation of
        block statement as a grammar
        rule.
        """
        statements = []

        while(self.tokens[self.index].get_token_type() != 'RIGHT_BRACE' and self.tokens[self.index].get_token_type() != 'EOF'):
            statements.append(self.declaration())
        
        self.consume('RIGHT_BRACE', "Expect \'}\' after block")
        return statements

    def expression_statement(self):
        """Representation of
        expression statement as a grammar rule.
        """
        expr = self.expression()
        self.consume('SEMICOLON', "Expect \';\' after expression")

        return Expression(expr)
    
    def return_statement(self):
        """Representation of a
        return statement as a grammar rule.
        """
        keyword = self.tokens[self.index - 1]
        value = None

        if self.tokens[self.index] != 'SEMICOLON':
            value = self.expression()
        
        self.consume('SEMICOLON', "Expect \';\' after return value")
        return Return(keyword, value)

    def expression(self):
        """Representation of expression
        as a grammar rule.
        """
        return self.assignment()
    
    def assignment(self):
        """Representation of assignment
        as a grammar rule.
        """
        expr = self.or_expression()

        if self.is_equal('EQUAL'):
            equals = self.tokens[self.index - 1]
            value = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)
            elif isinstance(expr, Get):
                get = expr
                return Set(get.lox_object, get.name, value)
            else:
                raise self.error(equals, "Invalid assignment target")
        else:    
            return expr

    def or_expression(self):
        """Representation of an
        or expression as a grammar rule.
        """
        expr = self.and_expression()

        while self.is_equal('OR'):
            operator = self.tokens[self.index - 1]
            right = self.and_expression()
            expr = Logical(expr, operator, right)
        
        return expr
    
    def and_expression(self):
        """Representation of an
        and expression as a grammar rule.
        """
        expr = self.equality()

        while self.is_equal('AND'):
            operator = self.tokens[self.index - 1]
            right = self.equality()
            expr = Logical(expr, operator, right)
        
        return expr

    def equality(self):
        """Representation of equality
        as a grammar rule.
        """
        expr = self.comparison()

        while(self.is_equal('NOT_EQUAL', 'EQUAL_EQUAL')):
            operator = self.tokens[self.index - 1]
            right_side = self.comparison()
            expr = Binary(expr, operator, right_side)
        return expr
    
    def comparison(self):
        """Representation of comparison
        as a grammar rule.
        """
        expr = self.term()

        while(self.is_equal('GREATER_THAN', 'GREATER_EQUAL', 'LESS_THAN', 'LESS_EQUAL')):
            operator = self.tokens[self.index - 1]
            right = self.term()
            expr = Binary(expr, operator, right)
        
        return expr
    
    def term(self):
        """Representation of term
        as a grammar rule.
        """
        expr = self.factor()

        while(self.is_equal('MINUS', 'PLUS')):
            operator = self.tokens[self.index - 1]
            right = self.factor()
            expr = Binary(expr, operator, right)
        
        return expr
    
    def factor(self):
        """Representation of factor
        as a grammar rule.
        """
        expr = self.unary()

        while(self.is_equal('SLASH', 'STAR')):
            operator = self.tokens[self.index - 1]
            right = self.unary()
            expr = Binary(expr, operator, right)
        
        return expr
    
    def unary(self):
        """Representation of unary
        as a grammar rule
        """
        if self.is_equal('NOT', 'MINUS'):
            operator = self.tokens[self.index - 1]
            right = self.unary()
            return Unary(operator, right)
        
        return self.call()
    
    def call(self):
        """Representation of a function
        call as a grammar rule.
        """
        expr = self.primary()

        while True:
            if self.is_equal('LEFT_PAREN'):
                expr = self.finish_call(expr)
            elif self.is_equal('DOT'):
                name = self.consume('IDENTIFIER', "Expect property name after \'.\'")
                expr = Get(expr, name)
            else:
                break
        
        return expr
    
    def finish_call(self, callee):
        """Parses the arguments inside
        the function call.
        """
        arguments = []

        if self.tokens[self.index].get_token_type() != 'RIGHT_PAREN':
            while True:
                if len(arguments) >= 255:
                    self.error(self.tokens[self.index], "Can\'t have more than 255 arguments")
                arguments.append(self.expression())
                if not self.is_equal('COMMA'):
                    break
        closing_paren = self.consume('RIGHT_PAREN', "Expect \')\' after arguments")

        return Call(callee, closing_paren, arguments)
    
    def primary(self):
        """Representation of primary
        as a grammar rule.
        """
        if self.is_equal('FALSE'):
            return Literal(False)
        if self.is_equal('TRUE'):
            return Literal(True)
        if self.is_equal('NIL'):
            return Literal(None)
        
        if self.is_equal('NUMBER', 'STRING'):
            return Literal(self.tokens[self.index - 1].get_literal())
        
        if self.is_equal('LEFT_PAREN'):
            expr = self.expression()
            self.consume('RIGHT_PAREN', "Expect \')\' after expression")
            return Grouping(expr)
        
        if self.is_equal('THIS'):
            return This(self.tokens[self.index - 1])
        
        if self.is_equal('IDENTIFIER'):
            return Variable(self.tokens[self.index - 1])
        
        if self.is_equal('SUPER'):
            keyword = self.tokens[self.index - 1]
            self.consume('DOT', "Expect \'.\' after \'super\'")
            method = self.consume('IDENTIFIER', "Expect superclass method name")
            return Super(keyword, method)
        
        raise self.error(self.tokens[self.index], "Expect expression")

    def is_equal(self, *types):
        """Determines whether a token
        matches with any of the given
        types.
        >>> from Token import Token
        >>> parser = Parser([Token("GREATER_THAN", 1, ">"), Token("GREATER_THAN", 1, ">")])
        >>> parser.is_equal("GREATER_THAN")
        True
        >>> parser.index
        1
        >>> parser.is_equal("LESS_THAN")
        False
        >>> parser.is_equal("LESS_THAN", "GREATER_THAN")
        True
        """
        for type in types:
            if self.tokens[self.index].get_token_type() != 'EOF' and self.tokens[self.index].get_token_type() == type:
                self.index += 1
                return True
        return False

    def consume(self, type, message):
        """Checks whether good syntax
        in parenthesis was followed,
        otherwise throws an error.
        """
        if self.tokens[self.index].get_token_type() != 'EOF' and self.tokens[self.index].get_token_type() == type:
            self.index += 1
            return self.tokens[self.index - 1]
        raise self.error(self.tokens[self.index], message)
    
    def error(self, token, message):
        """Displays error for user to
        handle.
        """
        self.lox_error = True
        return LoxError.error(token, message, self.tokens[self.index].get_token_type() == 'EOF')
    
    def synchronize(self):
        """Synchronizes the scanner
        after an error has been detected
        """
        if self.tokens[self.index].get_token_type() != 'EOF':
            self.index += 1

        while self.tokens[self.index].get_token_type() != 'EOF':
            if self.tokens[self.index - 1].get_token_type() == 'SEMICOLON':
                return None
            else:
                token_type = self.tokens[self.index].get_token_type()
                
                if token_type == 'CLASS' or token_type == 'FUN' or token_type == 'VAR' or token_type == 'FOR' or token_type == 'IF' or token_type == 'WHILE' or token_type == 'PRINT' or token_type == 'RETURN':
                    return None
                
            self.index += 1

if __name__ == '__main__':
    import doctest
    doctest.testmod()