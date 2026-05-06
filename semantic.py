from ast_nodes import *

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    
    # Entry Point
    def analyze(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')
    
    # Program
    def visit_Program(self, node):
        for stmt in node.statements:
            self.analyze(stmt)

    # Variable Declaration
    def visit_VarDecl(self, node):
        if node.name in self.symbol_table:
            raise Exception(f"Variable '{node.name}' already declared")

        value_type = self.analyze(node.value)

        if not self.type_compatible(node.var_type, value_type):
            raise Exception(
                f"Type mismatch: cannot assign {value_type} to {node.var_type}"
            )

        self.symbol_table[node.name] = node.var_type


    # Assignment
    def visit_Assign(self, node):
        if node.name not in self.symbol_table:
            raise Exception(f"Variable '{node.name}' not declared")

        value_type = self.analyze(node.value)
        var_type = self.symbol_table[node.name]

        if not self.type_compatible(var_type, value_type):
            raise Exception(
                f"Type mismatch: cannot assign {value_type} to {var_type}"
            )

    # Print
    def visit_Print(self, node):
        self.analyze(node.value)


    # Expressions
    def visit_BinOp(self, node):
        left_type = self.analyze(node.left)
        right_type = self.analyze(node.right)

        if left_type != right_type:
            raise Exception("Type mismatch in expression")

        return left_type

    def visit_Num(self, node):
        return 'FLOAT' if isinstance(node.value, float) else 'INT'

    def visit_Var(self, node):
        if node.name not in self.symbol_table:
            raise Exception(f"Variable '{node.name}' not declared")

        return self.symbol_table[node.name]

    
    # Type Checking Helper
    def type_compatible(self, declared, actual):
        if declared == 'FLOAT' and actual == 'INT':
            return True
        return declared == actual