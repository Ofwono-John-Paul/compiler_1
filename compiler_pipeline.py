from __future__ import annotations

import io
from contextlib import redirect_stdout
from typing import Any, Dict

from codegen import CodeGenerator
from lexer import Lexer
from optimizer import Optimizer
from parser import Parser
from semantic import SemanticAnalyzer


DEFAULT_SOURCE = """int x = 5 + 3;
int y = x * 2;
print(y);
"""


def ast_to_dict(node: Any) -> Dict[str, Any]:
    """Convert AST nodes into plain dicts that can be sent as JSON."""
    if node is None:
        return {"type": "None"}

    node_type = type(node).__name__
    data: Dict[str, Any] = {"type": node_type}

    if node_type == "Program":
        data["statements"] = [ast_to_dict(stmt) for stmt in node.statements]
    elif node_type == "VarDecl":
        data["var_type"] = node.var_type
        data["name"] = node.name
        data["value"] = ast_to_dict(node.value)
    elif node_type == "Assign":
        data["name"] = node.name
        data["value"] = ast_to_dict(node.value)
    elif node_type == "Print":
        data["value"] = ast_to_dict(node.value)
    elif node_type == "BinOp":
        data["operator"] = node.op
        data["left"] = ast_to_dict(node.left)
        data["right"] = ast_to_dict(node.right)
    elif node_type == "Num":
        data["value"] = node.value
    elif node_type == "Var":
        data["name"] = node.name

    return data


def compile_source(source_code: str) -> Dict[str, Any]:
    if not source_code or not source_code.strip():
        source_code = DEFAULT_SOURCE

    result: Dict[str, Any] = {
        "success": False,
        "error": None,
        "stage": None,
        "tokens": [],
        "parse_tree": None,
        "parse_tree_json": None,
        "symbol_table": {},
        "ast": None,
        "optimized_ast": None,
        "generated_code": "",
        "execution_output": "",
    }

    try:
        result["stage"] = "lexer"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        result["tokens"] = [
            {
                "type": t.type,
                "value": t.value,
                "line": t.line,
                "column": t.column,
            }
            for t in tokens
        ]

        result["stage"] = "parser"
        parser = Parser(tokens)
        ast = parser.parse()
        result["parse_tree"] = repr(ast)
        result["parse_tree_json"] = ast_to_dict(ast)
        result["ast"] = ast_to_dict(ast)

        result["stage"] = "semantic"
        semantic = SemanticAnalyzer()
        semantic.analyze(ast)
        result["symbol_table"] = dict(semantic.symbol_table)

        result["stage"] = "optimizer"
        optimizer = Optimizer()
        optimized_ast = optimizer.optimize(ast)
        result["optimized_ast"] = ast_to_dict(optimized_ast)

        result["stage"] = "codegen"
        generator = CodeGenerator()
        python_code = generator.generate(optimized_ast)
        result["generated_code"] = python_code

        result["stage"] = "execution"
        captured_stdout = io.StringIO()
        with redirect_stdout(captured_stdout):
            exec(python_code, {})
        result["execution_output"] = captured_stdout.getvalue()

        result["stage"] = "done"
        result["success"] = True
        return result

    except Exception as exc:  # noqa: BLE001
        result["error"] = str(exc)
        return result
