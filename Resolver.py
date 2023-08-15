from StmtVisitor import StmtVisitor
from ExprVisitor import ExprVisitor
import LoxError

class Resolver(StmtVisitor, ExprVisitor):
    def __init__(self, interpreter):
        """Instantiates an object
        of Resolver class given an interpreter
        object.
        >>> from Interpreter import Interpreter
        >>> interpreter = Interpreter(None)
        >>> resolver = Resolver(interpreter)
        >>> resolver.interpreter is interpreter
        True
        >>> resolver.interpreter = None
        >>> resolver.interpreter
        """
        self.interpreter = interpreter
        self.scopes = []
        self.current_function = "NONE"
        self.lox_error = False
        self.current_class = 'NONE'
    
    def resolve(self, statements):
        """Starts the resolver.
        """
        self.resolve_multiple_stmts(statements)

    def visit_class_stmt(self, statement):
        """Resolves a class statement.
        """
        enclosing_class = self.current_class
        self.current_class = 'CLASS'

        self.declare(statement.name)
        self.define(statement.name)

        if statement.superclass != None and statement.name.get_lexeme() == statement.superclass.name.get_lexeme():
            self.lox_error = True
            LoxError.error(statement.superclass.name, "A class can\'t inherit from itself", False)

        if statement.superclass != None:
            self.current_class = 'SUBCLASS'
            self.resolve_statement(statement.superclass)

        if statement.superclass != None:
            self.begin_scope()
            self.scopes[len(self.scopes) - 1]['super'] = True

        self.begin_scope()
        self.scopes[len(self.scopes) - 1]['this'] = True

        for method in statement.methods:
            declaration = 'METHOD'
            if method.name.get_lexeme() == 'init':
                declaration = 'INITIALIZER'

            self.resolve_function(method, declaration)

        self.end_scope()

        if statement.superclass != None:
            self.end_scope()

        self.current_class = enclosing_class
        return None

    def visit_block_stmt(self, statement):
        """Resolves the statements
        in the block statement.
        """
        self.begin_scope()
        self.resolve_multiple_stmts(statement.statements)
        self.end_scope()

        return None
    
    def visit_var_stmt(self, statement):
        """Resolves the var
        statement.
        """
        self.declare(statement.name)
        if statement.initializer != None:
            self.resolve_statement(statement.initializer)
        self.define(statement.name)

        return None
    
    def visit_function_stmt(self, statement):
        """Resolves a function statement.
        """
        self.declare(statement.name)
        self.define(statement.name)

        self.resolve_function(statement, "FUNCTION")

        return None
    
    def visit_expression_stmt(self, statement):
        """Resolves a expression statement.
        """
        self.resolve_statement(statement.expression)

        return None
    
    def visit_if_stmt(self, statement):
        """Resolves an if statement.
        """
        self.resolve_statement(statement.condition)
        self.resolve_statement(statement.then_branch)

        if statement.else_branch != None:
            self.resolve_statement(statement.else_branch)
        
        return None
    
    def visit_print_stmt(self, statement):
        """Resolves a print statement.
        """
        self.resolve_statement(statement.expression)

        return None
    
    def visit_return_stmt(self, statement):
        """Resolves a return statement.
        """
        if self.current_function == "NONE":
            self.lox_error = True
            LoxError.error(statement.keyword, "Can\'t return from top-level code", False)

        if statement.value != None:
            if self.current_function == 'INITIALIZER':
                self.lox_error = True
                LoxError.error(statement.keyword, "Can\'t return a value from an initializer", False)
            else:    
                self.resolve_statement(statement.value)
        
        return None
    
    def visit_while_stmt(self, statement):
        """Resolves a while statement.
        """
        self.resolve_statement(statement.condition)
        self.resolve_statement(statement.body)

        return None
    
    def visit_super_expr(self, expression):
        """Resolves a super expression.
        """
        if self.current_class == 'NONE':
            self.lox_error = True
            LoxError.error(expression.keyword, "Can\'t use \'super\' outside of a class", False)
        elif self.current_class != 'SUBCLASS':
            self.lox_error = True
            LoxError.error(expression.keyword, "Can\'t use \'super\' in a class with no superclass", False)
        else:
            self.resolve_local(expression, expression.keyword)
        return None
    
    def visit_binary_expr(self, expression):
        """Resolves a binary expression.
        """
        self.resolve_expression(expression.left)
        self.resolve_expression(expression.right)

        return None
    
    def visit_call_expr(self, expression):
        """Resolves a call expression.
        """
        self.resolve_expression(expression.callee)

        for argument in expression.arguments:
            self.resolve_expression(argument)
        
        return None
    
    def visit_get_expr(self, expression):
        """Resolves a get expression.
        """
        self.resolve_expression(expression.lox_object)

        return None
    
    def visit_set_expr(self, expression):
        """Resolves a set expression.
        """
        self.resolve_expression(expression.value)
        self.resolve_expression(expression.lox_object)

        return None

    def visit_grouping_expr(self, expression):
        """Resolves a grouping expression.
        """
        self.resolve_expression(expression.expression)

        return None
    
    def visit_this_expr(self, expression):
        """Resolves a this expression.
        """
        if self.current_class == 'NONE':
            self.lox_error = True
            LoxError.error(expression.keyword, "Can\'t use \'this\' outside of a class", False)
        else:
            self.resolve_local(expression, expression.keyword)
        
        return None
    
    def visit_literal_expr(self, expression):
        """Resolves a literal expression.
        """
        return None
    
    def visit_logical_expr(self, expression):
        """Resolves a logical expression.
        """
        self.resolve_expression(expression.left)
        self.resolve_expression(expression.right)

        return None
    
    def visit_unary_expr(self, expression):
        """Resolves an unary expression.
        """
        self.resolve_expression(expression.right)

        return None
    
    def resolve_function(self, function, function_type):
        """Resolves a function and define
        its name.
        """
        enclosing_function = self.current_function
        self.current_function = function_type

        self.begin_scope()
        for parameter in function.params:
            self.declare(parameter)
            self.define(parameter)
        self.resolve_multiple_stmts(function.body)
        self.end_scope()
        self.current_function = enclosing_function

    def visit_variable_expr(self, expression):
        """Resolves the variable
        expression.
        """
        if len(self.scopes) != 0 and self.scopes[len(self.scopes) - 1].get(expression.name.get_lexeme()) == False:
            self.lox_error = True
            LoxError.error(expression.name, "Can\'t read local variable in its own initializer", False)
        else:
            self.resolve_local(expression, expression.name)

        return None
    
    def visit_assign_expr(self, expression):
        """Resolves a assign expression.
        """
        self.resolve_expression(expression.value)
        self.resolve_local(expression, expression.name)

        return None
    
    def resolve_local(self, expression, name):
        """Looks for a match in the scopes field
        and resolves it after the match.
        """
        for i in reversed(range(len(self.scopes))):
            if name.get_lexeme() in self.scopes[i]:
                self.interpreter.resolve(expression, len(self.scopes) - 1 - i)
                return None
    
    def declare(self, name):
        """Given a token called name,
        it stores the lexeme of the token
        in the field stacks as the outermost dictionary
        and sets it to false.
        """
        if len(self.scopes) == 0:
            return None
        else:
            scope = self.scopes[len(self.scopes) - 1]
            if name.get_lexeme() in scope:
                self.lox_error = True
                LoxError.error(name, "Already a variable with this name in this scope", False)

            scope[name.get_lexeme()] = False
        
    def define(self, name):
        """Given token called name,
        it stores the lexeme of the token
        in the field stacks as the outermost
        dictionary and sets it to true.
        """
        if len(self.scopes) == 0:
            return None
        else:
            scope = self.scopes[len(self.scopes) - 1]
            scope[name.get_lexeme()] = True
    
    def resolve_multiple_stmts(self, statements):
        """For each statement in the
        parameter statements, it calls
        resolve statement to visit its
        accept method.
        """
        for statement in statements:
            self.resolve_statement(statement)
    
    def resolve_statement(self, statement):
        """Calls the accept method
        of statement to visit a
        node in the abstract syntax tree.
        """
        statement.accept(self)

    def resolve_expression(self, expr):
        """Calls the accept method
        of an expression to visit
        a node in the abstract syntax tree.
        """
        expr.accept(self)
    
    def begin_scope(self):
        """Tracks the stack of scopes within a scope.
        """
        self.scopes.append(dict())
    
    def end_scope(self):
        """Removes the outermost scope in the scopes
        field.
        """
        self.scopes.pop()

if __name__ == '__main__':
    import doctest
    doctest.testmod()