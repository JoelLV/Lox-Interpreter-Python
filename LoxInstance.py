from LoxError import LoxException as RuntimeException

class LoxInstance:
    def __init__(self, klass):
        """Initializes a LoxInstance
        object.
        """
        self.klass = klass
        self.fields = {}
    
    def __str__(self):
        """Returns a human readable
        string representing a LoxInstance
        object.
        """
        return f"{self.klass.name} instance"
    
    def get(self, name):
        """Gets the field or method given name.
        """
        if name.get_lexeme() in self.fields:
            return self.fields[name.get_lexeme()]
        else:
            method = self.klass.find_method(name.get_lexeme())
            if method != None:
                return method.bind(self)
            else:
                raise RuntimeException(name, f"Undefined property {name.get_lexeme()}.")
        
    def set(self, name, value):
        """Sets the field given name and value.
        """
        self.fields[name.get_lexeme()] = value