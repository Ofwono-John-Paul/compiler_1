from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, token_type):
        token = self.current_token()
        if token and token.type == token_type:
            self.pos += 1
            return token
        else:
            raise Exception(f"Expected {token_type}, got {token}")

    
    # Entry Point
    def parse(self):
        statements = []

        while self.current_token() is not None:
            statements.append(self.statement())

        return Program(statements)

    
    # Statements
    def statement(self):
        token = self.current_token()

        if token.type in ('INT', 'FLOAT', 'CHAR', 'DOUBLE'):
            return self.var_decl()

        elif token.type == 'IDENT':
            return self.assignment()

        elif token.type == 'PRINT':
            return self.print_stmt()

        else:
            raise Exception(f"Unexpected token: {token}")

    def var_decl(self):
        var_type = self.eat(self.current_token().type).type
        name = self.eat('IDENT').value
        self.eat('ASSIGN')
        value = self.expr()
        self.eat('SEMICOLON')
        return VarDecl(var_type, name, value)

    def assignment(self):
        name = self.eat('IDENT').value
        self.eat('ASSIGN')
        value = self.expr()
        self.eat('SEMICOLON')
        return Assign(name, value)

    def print_stmt(self):
        self.eat('PRINT')
        self.eat('LPAREN')
        value = self.expr()
        self.eat('RPAREN')
        self.eat('SEMICOLON')
        return Print(value)

    
    # Expressions
    def expr(self):
        node = self.term()

        while self.current_token() and self.current_token().type in ('PLUS', 'MINUS'):
            op = self.eat(self.current_token().type).type
            right = self.term()
            node = BinOp(node, op, right)

        return node

    def term(self):
        node = self.factor()

        while self.current_token() and self.current_token().type in ('MULT', 'DIV'):
            op = self.eat(self.current_token().type).type
            right = self.factor()
            node = BinOp(node, op, right)

        return node

    def factor(self):
        token = self.current_token()

        if token.type == 'NUMBER':
            return Num(self.eat('NUMBER').value)

        elif token.type == 'IDENT':
            return Var(self.eat('IDENT').value)

        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr()
            self.eat('RPAREN')
            return node

        else:
            raise Exception(f"Unexpected factor: {token}")