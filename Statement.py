from abc import ABC, abstractclassmethod

class Stmt(ABC):
    @abstractclassmethod
    def __init__(self):
        pass
    @abstractclassmethod
    def accept(self):
        pass