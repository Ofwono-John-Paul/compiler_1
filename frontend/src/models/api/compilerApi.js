export async function compileSource(source) {
  const response = await fetch("/api/compile", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ source }),
  });

  const payload = await response.json();

  if (!response.ok) {
    const message = payload?.error || payload?.result?.error || "Compilation failed";
    throw new Error(message);
  }

  return payload.result;
}
