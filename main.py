from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from optimizer import Optimizer
from codegen import CodeGenerator


 
# Input Program
 
code = """
int x = 5 + 3;
int y = x * 2;
print(y);
"""


 
# 1. Lexer
 
print("TOKENS")
lexer = Lexer(code)
tokens = lexer.tokenize()

for t in tokens:
    print(t)


 
# 2. Parser
 
print("\nAST (PARSE TREE)")
parser = Parser(tokens)
ast = parser.parse()
print(ast)


 
# 3. Semantic Analysis
 
print("\nSEMANTIC CHECK")
semantic = SemanticAnalyzer()
semantic.analyze(ast)
print("✔ Passed")


 
# 4. Optimizer
 
print("\nOPTIMIZED AST")
optimizer = Optimizer()
optimized_ast = optimizer.optimize(ast)
print(optimized_ast)


 
# 5. Code Generation
 
print("\nGENERATED CODE")
generator = CodeGenerator()
python_code = generator.generate(optimized_ast)
print(python_code)


 
# 6. Execution
 
print("\nEXECUTION OUTPUT")
exec(python_code)