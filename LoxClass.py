from LoxCallable import LoxCallable
from LoxInstance import LoxInstance

class LoxClass(LoxCallable):
    def __init__(self, name, superclass, methods):
        """Initializes a
        LoxClass object.
        """
        self.name = name
        self.superclass = superclass
        self.methods = methods
    
    def __str__(self):
        """Returns a human readable
        string representing a
        LoxClass object.
        """
        return self.name
    
    def call(self, interpreter, arguments):
        """Creates a new instance of a LoxClass.
        """
        instance = LoxInstance(self)
        initializer = self.find_method('init')
        if initializer != None:
            initializer.bind(instance).call(interpreter, arguments)

        return instance
    
    def arity(self):
        """Returns the arity of a
        LoxClass
        """
        initializer = self.find_method('init')
        if initializer == None:
            return 0
        else:
            return initializer.arity()
    
    def find_method(self, name):
        """Finds method given lexeme.
        """
        if name in self.methods:
            return self.methods[name]
        elif self.superclass != None:
            return self.superclass.find_method(name)
        else:
            return None