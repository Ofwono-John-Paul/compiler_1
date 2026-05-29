import { useCompilerController } from "../controllers/useCompilerController";
import StagePanel from "./components/StagePanel";
import TokenTable from "./components/TokenTable";
import TreeRenderer from "./components/TreeRenderer";

export default function App() {
  const {
    sourceCode,
    setSourceCode,
    isCompiling,
    error,
    stages,
    runCompilation,
  } = useCompilerController();

  const tokenStage = stages.find((stage) => stage.key === "tokens");
  const otherStages = stages.filter((stage) => stage.key !== "tokens");
  const treeKeys = new Set(["parse_tree", "ast", "optimized_ast"]);

  return (
    <div className="app-shell">
      <div className="bg-orb bg-orb-1" />
      <div className="bg-orb bg-orb-2" />

      <header className="hero">
        <p className="eyebrow">Compiler Design Lab</p>
        <h1>Compiler Stage Explorer</h1>
        <p className="subtitle">
          Compile code and inspect each stage: lexemes, parse tree, symbol table, and AST in one place.
        </p>
      </header>

      <main className="layout">
        <section className="editor-card">
          <h2>Source Code</h2>
          <textarea
            value={sourceCode}
            onChange={(event) => setSourceCode(event.target.value)}
            placeholder="Write your input program here"
          />
          <button type="button" onClick={runCompilation} disabled={isCompiling}>
            {isCompiling ? "Compiling..." : "Run Compiler"}
          </button>
          {error ? <p className="error-text">{error}</p> : null}
        </section>

        <section className="results-card">
          <h2>Lexemes / Tokens</h2>
          <TokenTable tokens={tokenStage?.data || []} />
        </section>
      </main>

      <section className="stages-grid">
        {otherStages.map((stage) => (
          treeKeys.has(stage.key) ? (
            <TreeRenderer key={stage.key} title={stage.title} data={stage.data} />
          ) : (
            <StagePanel key={stage.key} title={stage.title} data={stage.data} />
          )
        ))}
      </section>
    </div>
  );
}
