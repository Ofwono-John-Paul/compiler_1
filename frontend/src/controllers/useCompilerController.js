import { useMemo, useState } from "react";
import { compileSource } from "../models/api/compilerApi";

const defaultCode = `int x = 5 + 3;
int y = x * 2;
print(y);`;

export function useCompilerController() {
  const [sourceCode, setSourceCode] = useState(defaultCode);
  const [isCompiling, setIsCompiling] = useState(false);
  const [compileResult, setCompileResult] = useState(null);
  const [error, setError] = useState("");

  const stages = useMemo(() => {
    if (!compileResult) {
      return [];
    }

    return [
      { key: "tokens", title: "Lexemes / Tokens", data: compileResult.tokens },
      { key: "parse_tree", title: "Parse Tree", data: compileResult.parse_tree_json },
      { key: "symbol_table", title: "Symbol Table", data: compileResult.symbol_table },
      { key: "ast", title: "Abstract Syntax Tree", data: compileResult.ast },
      { key: "optimized_ast", title: "Optimized AST", data: compileResult.optimized_ast },
      { key: "generated_code", title: "Generated Python Code", data: compileResult.generated_code },
      { key: "execution_output", title: "Execution Output", data: compileResult.execution_output },
    ];
  }, [compileResult]);

  async function runCompilation() {
    setIsCompiling(true);
    setError("");

    try {
      const result = await compileSource(sourceCode);
      setCompileResult(result);
    } catch (err) {
      setCompileResult(null);
      setError(err.message || "Unexpected compiler error");
    } finally {
      setIsCompiling(false);
    }
  }

  return {
    sourceCode,
    setSourceCode,
    isCompiling,
    compileResult,
    error,
    stages,
    runCompilation,
  };
}
