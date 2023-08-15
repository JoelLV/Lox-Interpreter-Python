from LoxError import LoxException as RuntimeException

class Environment:
    def __init__(self, values = dict(), enclosing = None):
        """Initializes an Environment
        object with values as a field.
        >>> env = Environment()
        >>> env.values
        {}
        >>> env.enclosing
        >>> env = Environment({'a':10, 'b':20})
        >>> env.values
        {'a': 10, 'b': 20}
        >>> previous_env = env
        >>> env = Environment({'c':15}, previous_env)
        >>> env.values
        {'c': 15}
        >>> env.enclosing is previous_env
        True
        """
        self.values = dict(values)
        self.enclosing = enclosing
    
    def define(self, name, value):
        """Adds a new variable
        to the values dictionary
        >>> env = Environment()
        >>> env.define('a', 10)
        >>> env.values
        {'a': 10}
        >>> env = Environment({'a':10})
        >>> env.define('b', 20)
        >>> env.values
        {'a': 10, 'b': 20}
        """
        self.values[name] = value
    
    def get(self, name):
        """Returns the value of self.values
        given name.
        >>> env = Environment()
        >>> from Token import Token
        >>> env.define('a', 10)
        >>> env.get(Token('IDENTIFIER', 1, 'a', None))
        10
        >>> env = Environment(enclosing = env)
        >>> env.define('o', 20)
        >>> env.get(Token('IDENTIFIER', 1, 'a', None))
        10
        >>> env.get(Token('IDENTIFIER', 1, 'o', None))
        20
        """
        if name.get_lexeme() in self.values:
            return self.values[name.get_lexeme()]
        elif self.enclosing != None:
            return self.enclosing.get(name)
        else:
            raise RuntimeException(name, f"Undefined variable \'{name.get_lexeme()}\'")
    
    def assign(self, name, value):
        """Reassigns existing variables
        in dictionary values with
        new value.
        >>> from Token import Token
        >>> env = Environment({'a':10})
        >>> env.get(Token('IDENTIFIER', 1, 'a', None))
        10
        >>> env.assign(Token('IDENTIFIER', 1, 'a', None), 20)
        >>> env.get(Token('IDENTIFIER', 1, 'a', None))
        20
        >>> env = Environment(enclosing = env)
        >>> env.define('b', 5)
        >>> env.assign(Token('IDENTIFIER', 1, 'b', None), 10)
        >>> env.get(Token('IDENTIFIER', 1, 'b', None))
        10
        >>> env.get(Token('IDENTIFIER', 1, 'a', None))
        20
        """
        if name.get_lexeme() in self.values:
            self.values[name.get_lexeme()] = value
            return None
        elif self.enclosing != None:
            self.enclosing.assign(name, value)
            return None
        else:
            raise RuntimeException(name, f"Undefined variable \'{name.get_lexeme()}\'")
        
    def get_at(self, distance, name):
        """Calls the ancestor method and
        returns the value of a variable inside the
        values dictionary.
        """
        return self.ancestor(distance).values.get(name)
    
    def ancestor(self, distance):
        """Returns the local environment
        given the distance.
        """
        environment = self
        for __ in range(distance):
            environment = environment.enclosing
        
        return environment
    
    def assign_at(self, distance, name, value):
        """Assigns given variable with new
        value using distance.
        """
        self.ancestor(distance).values[name.get_lexeme()] = value

if __name__=='__main__':
    import doctest
    doctest.testmod()