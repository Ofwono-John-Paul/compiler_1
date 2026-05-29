export default function TokenTable({ tokens }) {
  if (!tokens || tokens.length === 0) {
    return <p className="empty-message">No tokens generated yet.</p>;
  }

  return (
    <div className="token-table-wrap">
      <table className="token-table">
        <thead>
          <tr>
            <th>Type</th>
            <th>Value</th>
            <th>Line</th>
            <th>Column</th>
          </tr>
        </thead>
        <tbody>
          {tokens.map((token, idx) => (
            <tr key={`${token.type}-${idx}`}>
              <td>{token.type}</td>
              <td>{String(token.value)}</td>
              <td>{token.line}</td>
              <td>{token.column}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
