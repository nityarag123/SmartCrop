/* ============================================================
   SmartCrop — pest.js (pest / disease detection)
   ============================================================ */

(function () {
  const severityClass = {
    "High": "sev-high",
    "Moderate": "sev-mod",
    "Low-Moderate": "sev-mod",
    "None for crops": "sev-low",
    "Unknown": "sev-low",
  };

  function renderResult(r) {
    const el = document.getElementById("pest-result");
    const severity = r.severity || "Unknown";
    const sev = severityClass[severity] || "sev-low";
    const confLabel = r.confidence_label ? ` (${r.confidence_label} confidence)` : "";
    const matches = (r.top_matches || []).map((m, i) =>
      `<span class="stat-pill ${i === 0 ? "stat-pill-primary" : ""}">${m.name} — ${Math.round(m.confidence * 100)}%</span>`
    ).join("");
    el.innerHTML = `
      <div class="card" style="margin-bottom:16px;">
        <div class="flex-between"><h3 data-i18n="pest.result">Detection result</h3><span class="tag">${r.engine || "AI"}</span></div>
        <h1 style="font-size:2rem;color:var(--green-700);margin:8px 0;">${r.label || r.detected_class || "—"}</h1>
        <div class="chip-row">
          <span class="stat-pill">Type: ${r.category || "—"}</span>
          <span class="stat-pill sev-pill ${sev}">Severity: ${severity}</span>
          <span class="stat-pill">Confidence: ${Math.round((r.confidence || 0) * 100)}%${confLabel}</span>
        </div>
        ${r.image ? `<p class="muted small">Uploaded file: ${r.image}</p>` : ""}
      </div>

      ${r.note ? `<div class="card" style="margin-bottom:16px;background:var(--green-50);"><p>ℹ️ ${r.note}</p></div>` : ""}
      ${matches ? `<div class="card" style="margin-bottom:16px;"><h3>Top matches</h3><div class="chip-row">${matches}</div></div>` : ""}

      ${r.symptoms ? `<div class="card" style="margin-bottom:16px;"><h3>🩺 <span data-i18n="pest.symptoms">Symptoms</span></h3><p>${r.symptoms}</p></div>` : ""}
      ${r.action ? `<div class="card" style="margin-bottom:16px;border-color:var(--amber);"><h3>✅ <span data-i18n="pest.action">What to do</span></h3><p>${r.action}</p></div>` : ""}
      ${r.prevention ? `<div class="card" style="margin-bottom:16px;background:var(--green-50);"><h3>🛡 <span data-i18n="pest.prevention">Prevention</span></h3><p>${r.prevention}</p></div>` : ""}
      ${r.pesticides && r.pesticides.length ? `<div class="card" style="margin-bottom:16px;border-color:var(--amber);background:#FFF8E1;"><h3>🧪 <span data-i18n="pest.pesticides">Recommended pesticides / chemicals</span></h3><ul style="margin:8px 0 8px 20px;line-height:1.7;">${r.pesticides.map((p) => `<li>${p}</li>`).join("")}</ul>${r.pesticide_note ? `<p class="muted small">⚠️ ${r.pesticide_note}</p>` : ""}</div>` : ""}`;
    el.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  document.addEventListener("DOMContentLoaded", () => {
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("pest-image");

    dropZone.addEventListener("click", () => fileInput.click());
    dropZone.addEventListener("dragover", (e) => { e.preventDefault(); dropZone.classList.add("dragover"); });
    dropZone.addEventListener("dragleave", () => dropZone.classList.remove("dragover"));
    dropZone.addEventListener("drop", (e) => {
      e.preventDefault();
      dropZone.classList.remove("dragover");
      if (e.dataTransfer.files.length) fileInput.files = e.dataTransfer.files;
      showPreview();
    });
    fileInput.addEventListener("change", showPreview);

    function showPreview() {
      const preview = document.getElementById("pest-preview");
      if (fileInput.files.length) {
        const file = fileInput.files[0];
        document.getElementById("pest-preview-img").src = URL.createObjectURL(file);
        document.getElementById("pest-file-name").textContent = file.name;
        preview.classList.remove("hidden");
      } else {
        preview.classList.add("hidden");
      }
    }

    document.getElementById("pest-form").addEventListener("submit", async (e) => {
      e.preventDefault();
      const alert = document.getElementById("pest-alert");
      alert.innerHTML = "";
      if (!fileInput.files.length) {
        alert.innerHTML = `<div class="alert alert-error">Please choose a photo first.</div>`;
        return;
      }
      const fd = new FormData();
      fd.append("image", fileInput.files[0]);
      const btn = document.getElementById("pest-btn");
      btn.disabled = true;
      btn.textContent = "Analyzing…";
      try {
        const result = await SmartCropAPI.detectPest(fd);
        renderResult(result);
      } catch (err) {
        alert.innerHTML = `<div class="alert alert-error">${err.message || "Could not analyze the image."}</div>`;
      } finally {
        btn.disabled = false;
        btn.textContent = "Detect Pest / Disease";
      }
    });
  });
})();
