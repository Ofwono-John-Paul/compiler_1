
class Program:
    def __init__(self, statements):
        self.statements = statements


class VarDecl:
    def __init__(self, var_type, name, value):
        self.var_type = var_type
        self.name = name
        self.value = value


class Assign:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Print:
    def __init__(self, value):
        self.value = value


class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Num:
    def __init__(self, value):
        self.value = value


class Var:
    def __init__(self, name):
        self.name = name