from ast_nodes import *

class CodeGenerator:
    def __init__(self):
        self.output = []

    
    # Entry Point
    
    def generate(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')


    # Program
    def visit_Program(self, node):
        for stmt in node.statements:
            self.generate(stmt)
        return "\n".join(self.output)

    
    # Statements
    def visit_VarDecl(self, node):
        code = f"{node.name} = {self.generate(node.value)}"
        self.output.append(code)

    def visit_Assign(self, node):
        code = f"{node.name} = {self.generate(node.value)}"
        self.output.append(code)

    def visit_Print(self, node):
        code = f"print({self.generate(node.value)})"
        self.output.append(code)

    
    # Expressions
    def visit_BinOp(self, node):
        left = self.generate(node.left)
        right = self.generate(node.right)

        op_map = {
            'PLUS': '+',
            'MINUS': '-',
            'MULT': '*',
            'DIV': '/'
        }

        op = op_map.get(node.op, node.op)
        return f"({left} {op} {right})"

    def visit_Num(self, node):
        return str(node.value)

    def visit_Var(self, node):
        return node.name