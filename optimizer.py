# optimizer.py

from ast_nodes import *

class Optimizer:
    def __init__(self):
        self.constants = {}  # symbol table for known constants

     
    # Entry Point
     
    def optimize(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        return node

     
    # Program
     
    def visit_Program(self, node):
        optimized_statements = []
        for stmt in node.statements:
            optimized_statements.append(self.optimize(stmt))
        node.statements = optimized_statements
        return node

     
    # Variable Declaration
     
    def visit_VarDecl(self, node):
        node.value = self.optimize(node.value)

        # Constant folding: int/float literals only
        if isinstance(node.value, Num):
            self.constants[node.name] = node.value.value

        return node

     
    # Assignment
     
    def visit_Assign(self, node):
        node.value = self.optimize(node.value)

        if isinstance(node.value, Num):
            self.constants[node.name] = node.value.value
        else:
            self.constants.pop(node.name, None)

        return node

     
    # Print
     
    def visit_Print(self, node):
        node.value = self.optimize(node.value)
        return node

     
    # Binary Operations (CORE OPTIMIZATION)
     
    def visit_BinOp(self, node):
        left = self.optimize(node.left)
        right = self.optimize(node.right)

        node.left = left
        node.right = right

        # Constant folding
        if isinstance(left, Num) and isinstance(right, Num):
            result = self.evaluate(node.op, left.value, right.value)
            return Num(result)

        return node

     
    # Variables
     
    def visit_Var(self, node):
        if node.name in self.constants:
            return Num(self.constants[node.name])
        return node

     
    # Numbers
     
    def visit_Num(self, node):
        return node

     
    # Helper: Evaluate operations
     
    def evaluate(self, op, left, right):
        if op == 'PLUS':
            return left + right
        elif op == 'MINUS':
            return left - right
        elif op == 'MULT':
            return left * right
        elif op == 'DIV':
            return left / right
        else:
            raise Exception(f"Unknown operator {op}")