import re
from dataclasses import dataclass

# Token Definition
 
@dataclass
class Token:
    type: str
    value: any
    line: int
    column: int

    def __repr__(self):
        return f"{self.type}:{self.value} (Line {self.line}, Col {self.column})"


 
# Lexer Class
 
class Lexer:
    KEYWORDS = {
        'int', 'float', 'char', 'double',
        'return', 'if', 'else', 'while',
        'for', 'void', 'print'
    }

    TOKEN_SPECIFICATION = [
        ('COMMENT',   r'//.*'),
        ('MCOMMENT',  r'/\*[\s\S]*?\*/'),
        ('STRING',    r'"[^"]*"'),
        ('NUMBER',    r'\d+(\.\d+)?'),

        ('EQ',        r'=='),
        ('NE',        r'!='),
        ('LE',        r'<='),
        ('GE',        r'>='),
        ('INC',       r'\+\+'),
        ('DEC',       r'--'),

        ('PLUS',      r'\+'),
        ('MINUS',     r'-'),
        ('MULT',      r'\*'),
        ('DIV',       r'/'),
        ('ASSIGN',    r'='),
        ('LT',        r'<'),
        ('GT',        r'>'),

        ('LPAREN',    r'\('),
        ('RPAREN',    r'\)'),
        ('LBRACE',    r'\{'),
        ('RBRACE',    r'\}'),
        ('LBRACKET',  r'\['),
        ('RBRACKET',  r'\]'),
        ('SEMICOLON', r';'),
        ('COMMA',     r','),

        ('IDENT',     r'[A-Za-z_]\w*'),

        ('NEWLINE',   r'\n'),
        ('SKIP',      r'[ \t]+'),
        ('MISMATCH',  r'.'),
    ]

    def __init__(self, text):
        self.text = text
        self.line = 1
        self.line_start = 0

        self.token_regex = '|'.join(
            f'(?P<{name}>{pattern})'
            for name, pattern in self.TOKEN_SPECIFICATION
        )

     
    # Tokenizer
     
    def tokenize(self):
        tokens = []

        for match in re.finditer(self.token_regex, self.text):
            kind = match.lastgroup
            value = match.group()
            column = match.start() - self.line_start

            # Handle new lines
            if kind == 'NEWLINE':
                self.line += 1
                self.line_start = match.end()
                continue

            # Skip whitespace and comments
            elif kind in ('SKIP', 'COMMENT', 'MCOMMENT'):
                continue

            # Handle identifiers and keywords
            elif kind == 'IDENT':
                if value in self.KEYWORDS:
                    kind = value.upper()   # e.g., 'if' → 'IF'
                else:
                    kind = 'IDENT'

            # Convert numbers
            elif kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)

            # Handle errors
            elif kind == 'MISMATCH':
                raise RuntimeError(
                    f'Unexpected character {value!r} at line {self.line}, column {column}'
                )

            tokens.append(Token(kind, value, self.line, column))

        return tokens