from abc import ABC, abstractclassmethod

class StmtVisitor(ABC):
    @abstractclassmethod
    def visit_var_stmt(expr):
        pass

    @abstractclassmethod
    def visit_if_stmt(expr):
        pass

    @abstractclassmethod
    def visit_expression_stmt(expr):
        pass

    @abstractclassmethod
    def visit_print_stmt(expr):
        pass

    @abstractclassmethod
    def visit_while_stmt(expr):
        pass

    @abstractclassmethod
    def visit_block_stmt(expr):
        pass

    @abstractclassmethod
    def visit_class_stmt(expr):
        pass

    @abstractclassmethod
    def visit_function_stmt(expr):
        pass

    @abstractclassmethod
    def visit_return_stmt(expr):
        pass

