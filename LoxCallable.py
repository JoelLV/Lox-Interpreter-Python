from abc import ABC, abstractclassmethod

class LoxCallable(ABC):
    @abstractclassmethod
    def call(self, interpreter, arguments):
        pass
    @abstractclassmethod
    def arity(self):
        pass