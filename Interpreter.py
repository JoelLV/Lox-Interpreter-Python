from LoxCallable import LoxCallable
from LoxClass import LoxClass
from LoxError import runtime_error, LoxException as RuntimeException
from LoxFunction import LoxFunction
from LoxInstance import LoxInstance
from ReturnException import Return
from ExprVisitor import ExprVisitor
from Environment import Environment
from Clock import ClockFunction
from StmtVisitor import StmtVisitor

class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self, tree):
        """Initializes an Interpreter object
        >>> interpreter = Interpreter(None)
        >>> str(interpreter.tree)
        'None'
        """
        self.tree = tree
        self.globals = Environment()
        self.environment = self.globals
        self.locals = {}

        self.globals.define("clock", ClockFunction())
        
    def interpret(self, statements):
        """Interprets given expression (Tested manually)
        """
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeException as error:
            runtime_error(error)
    
    def execute(self, statement):
        """Executes given statement. (Tested manually)
        """
        statement.accept(self)
    
    def stringify(self, value):
        """Returns a human readable
        string representing the
        result of the interpretation.
        >>> interpreter = Interpreter(None)
        >>> interpreter.stringify(None)
        'nil'
        >>> interpreter.stringify(2.0)
        '2'
        >>> interpreter.stringify(3.52)
        '3.52'
        >>> interpreter.stringify(True)
        'true'
        >>> interpreter.stringify(False)
        'false'
        >>> interpreter.stringify({})
        '{}'
        """
        if value == None:
            return "nil"
        elif isinstance(value, float):
            text = str(value)

            if text.endswith(".0"):
                text = text[:len(text) - 2]
                return text
        
        elif isinstance(value, bool):
            return str(value).lower()
            
        return str(value)
    
    def visit_class_stmt(self, statement):
        """Evaluates a class statement.
        """
        superclass = None
        if statement.superclass != None:
            superclass = self.evaluate(statement.superclass)
            if not isinstance(superclass, LoxClass):
                raise RuntimeException(statement.superclass.name, "Superclass must be a class")
        self.environment.define(statement.name.get_lexeme(), None)

        if statement.superclass != None:
            self.environment = Environment(enclosing = self.environment)
            self.environment.define('super', superclass)

        methods = {}
        for method in statement.methods:
            method_is_initializer = method.name.get_lexeme() == 'init'
            function = LoxFunction(method, self.environment, is_initializer = method_is_initializer)
            methods[method.name.get_lexeme()] = function
        klass = LoxClass(statement.name.get_lexeme(), superclass, methods)

        if superclass != None:
            self.environment = self.environment.enclosing

        self.environment.assign(statement.name, klass)

    def visit_variable_expr(self, expr):
        """Returns the evaluation of
        the variable expression.
        """
        return self.look_up_variable(expr.name, expr)
    
    def resolve(self, expr, depth):
        """Inserts an expression
        into the locals dictionary
        with a depth value.
        """
        self.locals[expr] = depth

    def look_up_variable(self, name, expr):
        """Looks up variables given the current
        environment.
        """
        if expr in self.locals:
            distance = self.locals[expr]
        else:
            distance = None
        if distance != None:
            return self.environment.get_at(distance, name.get_lexeme())
        else:
            return self.globals.get(name)

    def visit_var_stmt(self, statement):
        """Returns the evaluation of
        the variable declaration statement.
        """
        value = None
        if statement.initializer != None:
            value = self.evaluate(statement.initializer)
        
        self.environment.define(statement.name.get_lexeme(), value)

        return None
    
    def visit_if_stmt(self, statement):
        """Returns the evaluation of
        the if statement.
        """
        if self.is_truthy(self.evaluate(statement.condition)):
            self.execute(statement.then_branch)
        elif statement.else_branch != None:
            self.execute(statement.else_branch)

        return None

    def visit_expression_stmt(self, statement):
        """Returns the evaluation of
        the expression statement.
        """
        self.evaluate(statement.expression)

        return None
    
    def visit_print_stmt(self, statement):
        """Returns the evaluation
        of the print statement.
        """
        value = self.evaluate(statement.expression)
        print(self.stringify(value))

        return None
    
    def visit_while_stmt(self, statement):
        """Returns the evaluation
        of a while statement.
        """
        while self.is_truthy(self.evaluate(statement.condition)):
            self.execute(statement.body)
        
        return None
    
    def visit_block_stmt(self, statement):
        """Calls execute_block method to
        execute all statements within
        the block.
        """
        self.execute_block(statement.statements, Environment(enclosing = self.environment))

        return None
    
    def visit_function_stmt(self, statement):
        """Creates a LoxFunction object and
        defines an environment.
        """
        function = LoxFunction(statement, self.environment)
        self.environment.define(statement.name.get_lexeme(), function)

        return None
    
    def visit_return_stmt(self, statement):
        """Executes the return statement
        by raising an exception with
        a Return object attached to it.
        """
        value = None
        if statement.value != None:
            value = self.evaluate(statement.value)
        
        raise Return(value)
    
    def execute_block(self, statements, environment):
        """Executes all statements
        within the block.
        """
        previous_environment = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous_environment

    def visit_super_expr(self, expr):
        """Executes a super expression.
        """
        distance = self.locals[expr]
        superclass = self.environment.get_at(distance, 'super')
        lox_object = self.environment.get_at(distance - 1, 'this')
        
        method = superclass.find_method(expr.method.get_lexeme())

        if method == None:
            raise RuntimeException(expr.method, f"Undefined property \'{expr.method.get_lexeme()}\'")
        return method.bind(lox_object)

    def visit_set_expr(self, expr):
        """Executes a set expression.
        """
        lox_object = self.evaluate(expr.lox_object)

        if not isinstance(lox_object, LoxInstance):
            raise RuntimeException(expr.name, "Only instances have fields.")
        
        value = self.evaluate(expr.value)
        lox_object.set(expr.name, value)

        return value

    def visit_get_expr(self, expr):
        """Executes a get expression.
        """
        lox_object = self.evaluate(expr.lox_object)
        if isinstance(lox_object, LoxInstance):
            return lox_object.get(expr.name)
        else:
            raise RuntimeException("Only instances have properties.")

    def visit_logical_expr(self, expr):
        """Executes a logical expression
        """
        left = self.evaluate(expr.left)

        if expr.operator.get_token_type() == 'OR':
            if self.is_truthy(left):
                return left
        elif expr.operator.get_token_type() == 'AND':
            if not self.is_truthy(left):
                return left
        
        return self.evaluate(expr.right)

    def visit_assign_expr(self, expr):
        """Returns the evaluation of a
        assignment expression.
        """
        value = self.evaluate(expr.value)
        
        distance = self.locals.get(expr)
        if distance != None:
            self.environment.assign_at(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)

        return value
    
    def visit_this_expr(self, expr):
        """Returns the evaluation of a
        this expression.
        """
        return self.look_up_variable(expr.keyword, expr)

    def visit_literal_expr(self, expr):
        """Returns the value of a
        literal expression.
        """
        return expr.value

    def visit_grouping_expr(self, expr):
        """Returns the evaluation
        of the expression enclosed
        in parenthesis.
        """
        return self.evaluate(expr.expression)

    def evaluate(self, expr):
        """Evaluates expression
        using the method accept
        from the Expression object.
        """
        return expr.accept(self)
    
    def visit_unary_expr(self, expr):
        """Returns the representation
        of a unary expression.
        """
        right = self.evaluate(expr.right)

        if expr.operator.get_token_type() == 'MINUS':
            self.check_number_operand(expr.operator, right)
            return -float(right)
        elif expr.operator.get_token_type() == 'NOT':
            return not self.is_truthy(right)
        
        return None
    
    def visit_call_expr(self, expr):
        """Evaluates call expression.
        """
        callee = self.evaluate(expr.callee)

        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))
        
        if not isinstance(callee, LoxCallable):
            raise RuntimeException(expr.paren, "Can only call functions and classes")
        function = callee

        if len(arguments) != function.arity():
            raise RuntimeException(expr.paren, f"Expected {function.arity()} arguments but got {len(arguments)}")

        return function.call(self, arguments)
    
    def is_truthy(self, obj):
        """Determines whether the object
        is truthy or falsey.
        >>> interpreter = Interpreter(None)
        >>> interpreter.is_truthy(None)
        False
        >>> interpreter.is_truthy(False)
        False
        >>> interpreter.is_truthy(True)
        True
        >>> interpreter.is_truthy("something")
        True
        """
        if obj == None:
            return False
        elif isinstance(obj, bool):
            return bool(obj)

        return True
    
    def visit_binary_expr(self, expr):
        """Returns the representation
        of a binary expression.
        """
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.get_token_type() == 'MINUS':
            self.check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        elif expr.operator.get_token_type() == 'SLASH':
            self.check_number_operands(expr.operator, left, right)
            return float(left) / float(right)
        elif expr.operator.get_token_type() == 'STAR':
            self.check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        elif expr.operator.get_token_type() == 'PLUS':
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            elif isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
            raise RuntimeException(expr.operator, "Operands must be two numbers or two strings.")
        elif expr.operator.get_token_type() == 'GREATER_THAN':
            self.check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        elif expr.operator.get_token_type() == 'GREATER_EQUAL':
            self.check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        elif expr.operator.get_token_type() == 'LESS_THAN':
            self.check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        elif expr.operator.get_token_type() == 'LESS_EQUAL':
            self.check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)
        elif expr.operator.get_token_type() == 'NOT_EQUAL':
            return not self.is_equal(left, right)
        elif expr.operator.get_token_type() == 'EQUAL_EQUAL':
            return self.is_equal(left, right)
        
        return None
    
    def is_equal(self, left, right):
        """Checks if left and right
        are equal according to the
        rules of the Lox language
        >>> interpreter = Interpreter(None)
        >>> interpreter.is_equal(None, None)
        True
        >>> interpreter.is_equal(None, "Something")
        False
        >>> interpreter.is_equal(2, 2)
        True
        >>> interpreter.is_equal("Something", "SomethingElse")
        False
        """
        if left == None and right == None:
            return True
        elif left == None:
            return False
        
        return left == right
    
    def check_number_operand(self, operator, operand):
        """Checks if operand is a number. Otherwise
        it throws an exception.
        """
        if isinstance(operand, float):
            return
        raise RuntimeException(operator, "Operand must be a number.")
    
    def check_number_operands(self, operator, left, right):
        """Checks if both left and right
        are numbers, otherwise it throws an
        exception.
        """
        if isinstance(left, float) and isinstance(right, float):
            return
        raise RuntimeException(operator, "Operands must be numbers.")

if __name__ == '__main__':
    import doctest
    doctest.testmod()