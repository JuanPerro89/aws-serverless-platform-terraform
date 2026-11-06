document.getElementById("btn").addEventListener("click", async () => {
  const out = document.getElementById("out");
  out.textContent = "";
  try {
    const res = await fetch(`${window.API_URL}/shorten`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: document.getElementById("url").value }),
    });
    if (!res.ok) throw new Error(res.status);
    const data = await res.json();
    const a = document.createElement("a");
    a.href = data.shortUrl;
    a.textContent = data.shortUrl;
    out.appendChild(a);
  } catch (e) {
    out.textContent = "Error al acortar la URL";
  }
});