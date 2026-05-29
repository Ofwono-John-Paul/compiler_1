import { useState } from "react";

function PrimitiveNode({ label, value }) {
  return (
    <div className="tree-primitive">
      <span className="tree-label">{label}</span>
      <span className="tree-sep">:</span>
      <span className="tree-value">{String(value)}</span>
    </div>
  );
}

function TreeNode({ label, value, depth = 0 }) {
  const isObject = value !== null && typeof value === "object";
  const isArray = Array.isArray(value);
  const [collapsed, setCollapsed] = useState(depth > 1);

  if (!isObject) {
    return <PrimitiveNode label={label} value={value} />;
  }

  const entries = isArray
    ? value.map((item, index) => [String(index), item])
    : Object.entries(value);

  return (
    <div className="tree-node-wrap">
      <button
        type="button"
        className="tree-toggle"
        onClick={() => setCollapsed((v) => !v)}
      >
        <span className="tree-caret">{collapsed ? "▸" : "▾"}</span>
        <span className="tree-label">{label}</span>
        <span className="tree-kind">{isArray ? "[ ]" : "{ }"}</span>
      </button>

      {!collapsed ? (
        <div className="tree-children">
          {entries.length === 0 ? (
            <p className="tree-empty">(empty)</p>
          ) : (
            entries.map(([childLabel, childValue]) => (
              <TreeNode
                key={`${label}-${childLabel}`}
                label={childLabel}
                value={childValue}
                depth={depth + 1}
              />
            ))
          )}
        </div>
      ) : null}
    </div>
  );
}

export default function TreeRenderer({ title, data }) {
  if (!data) {
    return (
      <section className="stage-panel">
        <h3>{title}</h3>
        <p className="empty-message">No tree available yet.</p>
      </section>
    );
  }

  return (
    <section className="stage-panel">
      <h3>{title}</h3>
      <div className="tree-surface">
        <TreeNode label="root" value={data} depth={0} />
      </div>
    </section>
  );
}
