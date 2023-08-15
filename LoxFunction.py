from LoxCallable import LoxCallable
from Environment import Environment
from ReturnException import Return

class LoxFunction(LoxCallable):
    def __init__(self, declaration, closure = None, is_initializer = False):
        """Initializes a LoxFunction
        object.
        """
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer
    
    def call(self, interpreter, arguments):
        """Implements the method call
        from the abstract class LoxCallable.
        Creates a new environment relative
        to the function and executes the function.
        """
        environment = Environment(enclosing = self.closure)

        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].get_lexeme(), arguments[i])    
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as return_value:
            if self.is_initializer:
                return self.closure.get_at(0, 'this')
            else:
                return return_value.value
        
        if self.is_initializer:
            return self.closure.get_at(0, 'this')
        else:
            return None
    
    def arity(self):
        """Determines the arity of the function.
        """
        return len(self.declaration.params)
    
    def __str__(self):
        """Returns a human readable string
        representing the object LoxFunction.
        """
        return f"<fn {self.declaration.name.get_lexeme()}>"
    
    def bind(self, instance):
        """Binds a dedicated environment
        to this instance.
        """
        environment = Environment(enclosing = self.closure)
        environment.define('this', instance)
        
        return LoxFunction(self.declaration, environment, is_initializer = self.is_initializer)