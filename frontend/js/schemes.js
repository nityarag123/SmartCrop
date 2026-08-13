/* ============================================================
   SmartCrop — schemes.js (government schemes)
   ============================================================ */

(function () {
  function render(schemes) {
    const list = document.getElementById("schemes-list");
    if (!schemes || !schemes.length) {
      list.innerHTML = `<div class="card state-box" style="grid-column:1/-1;">No schemes found.</div>`;
      return;
    }
    list.innerHTML = schemes.map((s) => `
      <div class="card" style="display:flex;flex-direction:column;">
        <div class="flex-between">
          <span class="tag ${s.category === "Central" ? "" : "tag-warning"}">${s.category || ""}</span>
          <span class="muted small">${s.code || ""}</span>
        </div>
        <h3 style="margin:10px 0 6px;">${s.name}</h3>
        <p class="muted">${s.summary || ""}</p>
        <div class="benefits-box"><b>🎁 ${"Benefits"}</b><p>${s.benefits || ""}</p></div>
        ${s.eligibility && s.eligibility.length ? `
          <b class="mt-2">${"Eligibility"}</b>
          <ul class="check-list">${s.eligibility.map((e) => `<li>${e}</li>`).join("")}</ul>` : ""}
        ${s.documents && s.documents.length ? `
          <b class="mt-2">${"Documents"}</b>
          <p class="muted small">${s.documents.join(" · ")}</p>` : ""}
        <div class="mt-2 process-box"><b>📝 ${"How to apply"}</b><p class="muted small">${s.process || ""}</p></div>
        ${s.source ? `<a class="small" href="${s.source}" target="_blank" rel="noopener">${"Official source"} ↗</a>` : ""}
      </div>`).join("");
  }

  async function load(filters) {
    const alert = document.getElementById("schemes-alert");
    alert.innerHTML = "";
    try {
      const data = await SmartCropAPI.getSchemes(filters);
      render(data.schemes || []);
    } catch (err) {
      alert.innerHTML = `<div class="alert alert-error">${err.message || "Could not load schemes."}</div>`;
      document.getElementById("schemes-list").innerHTML = "";
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("s-search").addEventListener("click", () => {
      load({ q: document.getElementById("s-q").value.trim(), category: document.getElementById("s-cat").value });
    });
    document.getElementById("s-q").addEventListener("keydown", (e) => {
      if (e.key === "Enter") { e.preventDefault(); document.getElementById("s-search").click(); }
    });
    document.getElementById("s-cat").addEventListener("change", () => document.getElementById("s-search").click());
    load({});
  });
})();
