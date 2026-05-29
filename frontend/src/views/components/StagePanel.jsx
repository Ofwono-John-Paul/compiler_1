export default function StagePanel({ title, data }) {
  const rendered = typeof data === "string" ? data : JSON.stringify(data, null, 2);

  return (
    <section className="stage-panel">
      <h3>{title}</h3>
      <pre>{rendered || "(empty)"}</pre>
    </section>
  );
}
