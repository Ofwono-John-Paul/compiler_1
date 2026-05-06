from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from optimizer import Optimizer
from codegen import CodeGenerator

code = """
int x = 5 + 3;
int y = x * 2;
print(y);
print(x);
"""

# 1. Lex
lexer = Lexer(code)
tokens = lexer.tokenize()

# 2. Parse
parser = Parser(tokens)
ast = parser.parse()

# 3. Semantic check
semantic = SemanticAnalyzer()
semantic.analyze(ast)

# 4. Optimize AST
optimizer = Optimizer()
ast = optimizer.optimize(ast)

# 5. Generate code
generator = CodeGenerator()
python_code = generator.generate(ast)

print("Optimized Output:\n")
print(python_code)

exec(python_code)