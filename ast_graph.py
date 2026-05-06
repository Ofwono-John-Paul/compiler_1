from graphviz import Digraph
from ast_nodes import *

class ASTGraph:
    def __init__(self):
        self.graph = Digraph()
        self.counter = 0

    def new_id(self):
        self.counter += 1
        return str(self.counter)

    def build(self, node):
        node_id = self.new_id()

        if isinstance(node, Program):
            self.graph.node(node_id, "Program")
            for stmt in node.statements:
                child_id = self.build(stmt)
                self.graph.edge(node_id, child_id)

        elif isinstance(node, VarDecl):
            self.graph.node(node_id, f"{node.var_type} {node.name}")
            child_id = self.build(node.value)
            self.graph.edge(node_id, child_id)

        elif isinstance(node, Assign):
            self.graph.node(node_id, f"Assign {node.name}")
            child_id = self.build(node.value)
            self.graph.edge(node_id, child_id)

        elif isinstance(node, Print):
            self.graph.node(node_id, "Print")
            child_id = self.build(node.value)
            self.graph.edge(node_id, child_id)

        elif isinstance(node, BinOp):
            self.graph.node(node_id, node.op)
            left_id = self.build(node.left)
            right_id = self.build(node.right)
            self.graph.edge(node_id, left_id)
            self.graph.edge(node_id, right_id)

        elif isinstance(node, Num):
            self.graph.node(node_id, str(node.value))

        elif isinstance(node, Var):
            self.graph.node(node_id, node.name)

        return node_id

    def render(self, filename="ast"):
        self.graph.render(filename, view=True)