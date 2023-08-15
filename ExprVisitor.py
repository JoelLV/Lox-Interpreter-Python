from abc import ABC, abstractclassmethod

class ExprVisitor(ABC):
    @abstractclassmethod
    def visit_binary_expr(expr):
        pass

    @abstractclassmethod
    def visit_grouping_expr(expr):
        pass

    @abstractclassmethod
    def visit_literal_expr(expr):
        pass

    @abstractclassmethod
    def visit_unary_expr(expr):
        pass

    @abstractclassmethod
    def visit_logical_expr(expr):
        pass

    @abstractclassmethod
    def visit_variable_expr(expr):
        pass

    @abstractclassmethod
    def visit_assign_expr(expr):
        pass

    @abstractclassmethod
    def visit_get_expr(expr):
        pass

    @abstractclassmethod
    def visit_set_expr(expr):
        pass

    @abstractclassmethod
    def visit_call_expr(expr):
        pass

    @abstractclassmethod
    def visit_this_expr(expr):
        pass

