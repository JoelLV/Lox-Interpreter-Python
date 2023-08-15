EXPRESSION_SUBCLASS_NAMES_FIELDS = {
    "Assign":["name", "value"],
    "Binary":["left", "operator", "right"],
    "Call":["callee", "paren", "arguments"],
    "Get":["object", "name"],
    "Grouping":["expression"],
    "Literal":["value"],
    "Logical":["left", "operator", "right"],
    "Set":["object", "name", "value"],
    "Super":["keyword", "method"],
    "This":["keyword"],
    "Unary":["operator", "right"],
    "Variable":["name"],
    "Logical":["left", "operator", "right"],
    "Get":["lox_object", "name"],
    "Set":["lox_object", "name", "value"]
}

EXPRESSION_VISITOR_METHODS = (
    "visit_binary_expr",
    "visit_grouping_expr",
    "visit_literal_expr",
    "visit_unary_expr",
    "visit_logical_expr",
    "visit_variable_expr",
    "visit_assign_expr",
    "visit_get_expr",
    "visit_set_expr",
    "visit_call_expr",
    "visit_this_expr"
)
STATEMENT_VISITOR_METHODS = (
    "visit_var_stmt",
    "visit_if_stmt",
    "visit_expression_stmt",
    "visit_print_stmt",
    "visit_while_stmt",
    "visit_block_stmt",
    "visit_class_stmt",
    "visit_function_stmt",
    "visit_return_stmt"
)
STATEMENT_SUBCLASS_NAMES_FIELDS = {
    "Block":["statements"],
    "Class":["name", "superclass", "methods"],
    "Expression":["expression"],
    "If":["condition", "then_branch", "else_branch"],
    "Function":["name", "params", "body"],
    "Print":["expression"],
    "Return":["keyword", "value"],
    "While":["condition", "body"],
    "Var":["name", "initializer"]
}

def generate_expression_classes(base_class, file_name, class_names):
    """Opens a file with the name
    ExprSubClasses and will write
    a bunch of classes, each representing
    the data inside the global
    dictionary SUBCLASS_NAMES_FIELDS
    """
    with open(file_name, 'w') as file:
        if base_class == 'Expr':
            file.write(f"from Expression import Expr\n\n")
        else:
            file.write(f"from Statement import Stmt\n\n")
        for expr_class in class_names:
            class_name = expr_class
            class_fields = class_names[expr_class]
            
            file.write(f"class {class_name}({base_class}):\n")
            file.write(f"    def __init__(self")
            for class_field in class_fields:
                file.write(f", {class_field}")
            file.write(f"):\n")
            for class_field in class_fields:
                file.write(f"       self.{class_field} = {class_field}\n")
            file.write("    def accept(self, visitor):\n")
            file.write(f"        return visitor.visit_{class_name[0].lower() + class_name[1:]}_{base_class.lower()}(self)\n")
            file.write("\n")

def generate_visitor_class(visitor_type, methods):
    """Opens a file with the name
    Visitor.py and will write
    a bunch of abstract methods
    for class Visitor from
    the global dictionary
    VISITOR_METHODS
    """
    with open(F"{visitor_type}.py", 'w') as file:
        file.write("from abc import ABC, abstractclassmethod\n\n")
        file.write(f"class {visitor_type}(ABC):\n")
        for method in methods:
            file.write("    @abstractclassmethod\n")
            file.write(f"    def {method}(expr):\n")
            file.write(f"        pass\n\n")

generate_expression_classes("Expr", "ExprSubClasses.py", EXPRESSION_SUBCLASS_NAMES_FIELDS)
generate_expression_classes("Stmt", "StmtSubClasses.py", STATEMENT_SUBCLASS_NAMES_FIELDS)
generate_visitor_class("ExprVisitor", EXPRESSION_VISITOR_METHODS)
generate_visitor_class("StmtVisitor", STATEMENT_VISITOR_METHODS)