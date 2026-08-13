/* ============================================================
   SmartCrop — soil.js
   ============================================================ */

(function () {
  function nutrientBar(label, item) {
    const statusClass = item.status === "low" ? "bar-red" : item.status === "high" ? "bar-amber" : "bar-green";
    const pct = Math.max(6, Math.min(100, item.percent || 0));
    return `
      <div class="nutrient-row">
        <div class="nutrient-top"><b>${label}</b><span>${item.value} — <span class="nut-status ${statusClass}">${item.label}</span></span></div>
        <div class="nutrient-track"><div class="nutrient-fill ${statusClass}" style="width:${pct}%"></div></div>
      </div>`;
  }

  function renderResult(r) {
    const el = document.getElementById("soil-result");
    const phStatusClass = r.ph.status === "low" ? "bar-red" : r.ph.status === "high" ? "bar-amber" : "bar-green";
    el.innerHTML = `
      <div class="card" style="margin-bottom:16px;">
        <div class="flex-between"><h3 data-i18n="soil.verdict">Soil Health Verdict</h3><span class="tag tag-warning">${r.engine}</span></div>
        <p class="lead" style="font-size:1.2rem;color:var(--green-700);font-weight:700;">${r.overall}</p>
        <p class="muted small">${r.engine_note}</p>
      </div>

      <div class="card" style="margin-bottom:16px;">
        <h3 data-i18n="soil.nutrients">Nutrient levels</h3>
        ${nutrientBar("Nitrogen (N)", r.nitrogen)}
        ${nutrientBar("Phosphorus (P)", r.phosphorus)}
        ${nutrientBar("Potassium (K)", r.potassium)}
        <div class="nutrient-row">
          <div class="nutrient-top"><b>Soil pH</b><span>${r.ph.value} — <span class="nut-status ${phStatusClass}">${r.ph.label}</span></span></div>
          <div class="nutrient-track"><div class="nutrient-fill ${phStatusClass}" style="width:${Math.max(6, Math.min(100, r.ph.percent || 0))}%"></div></div>
        </div>
        <div class="nutrient-row">
          <div class="nutrient-top"><b>Moisture</b><span>${r.moisture.value}% — <span class="nut-status">${r.moisture.label}</span></span></div>
        </div>
      </div>

      <div class="card" style="margin-bottom:16px;">
        <h3 data-i18n="soil.suitableCrops">Suitable crops</h3>
        <div class="chip-row">${(r.suitable_crops || []).map((c) => `<span class="stat-pill">🌾 ${c}</span>`).join("") || `<span class="muted">—</span>`}</div>
      </div>

      <div class="card">
        <h3 data-i18n="soil.guidance">Fertiliser guidance</h3>
        <ul class="check-list">${(r.fertilizer_guidance || []).map((g) => `<li>${g}</li>`).join("")}</ul>
      </div>`;
    el.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function imageNutrientBar(label, item) {
    const statusClass = item.status === "low" ? "bar-red" : item.status === "high" ? "bar-amber" : "bar-green";
    const pct = Math.max(6, Math.min(100, item.percent || 0));
    return `
      <div class="nutrient-row">
        <div class="nutrient-top"><b>${label}</b><span><span class="nut-status ${statusClass}">${item.label}</span></span></div>
        <div class="nutrient-track"><div class="nutrient-fill ${statusClass}" style="width:${pct}%"></div></div>
        ${item.note ? `<p class="muted small" style="margin:4px 0 0;">${item.note}</p>` : ""}
      </div>`;
  }

  function renderImageResult(r) {
    const el = document.getElementById("soil-result");
    el.innerHTML = `
      <div class="card" style="margin-bottom:16px;">
        <div class="flex-between"><h3 data-i18n="soil.imageResult">Soil photo analysis</h3><span class="tag tag-warning">${r.engine}</span></div>
        <h2 style="color:var(--green-700);margin:6px 0;">🪨 ${r.soil_color}</h2>
        <div class="chip-row">
          <span class="stat-pill">🧱 ${r.texture}</span>
        </div>
        <p class="muted small" style="margin-top:10px;">🟤 ${r.organic_matter}</p>
        <p class="muted small">💧 ${r.drainage}</p>
      </div>

      <div class="card" style="margin-bottom:16px;">
        <h3>Likely nutrient levels <span class="muted small">(visual estimate)</span></h3>
        ${imageNutrientBar("Nitrogen (N)", r.likely_nutrients.n)}
        ${imageNutrientBar("Phosphorus (P)", r.likely_nutrients.p)}
        ${imageNutrientBar("Potassium (K)", r.likely_nutrients.k)}
        ${imageNutrientBar("Soil pH", r.likely_nutrients.ph)}
      </div>

      <div class="card" style="margin-bottom:16px;">
        <h3 data-i18n="soil.suitableCrops">Suitable crops</h3>
        <div class="chip-row">${(r.suitable_crops || []).map((c) => `<span class="stat-pill">🌾 ${c}</span>`).join("") || `<span class="muted">—</span>`}</div>
      </div>

      <div class="card" style="margin-bottom:16px;">
        <h3 data-i18n="soil.guidance">Guidance</h3>
        <ul class="check-list">${(r.guidance || []).map((g) => `<li>${g}</li>`).join("")}</ul>
      </div>

      <div class="alert alert-warning">${r.engine_note}</div>`;
    el.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("soil-form");
    const btn = document.getElementById("soil-btn");
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const alert = document.getElementById("soil-alert");
      alert.innerHTML = "";
      const body = {
        nitrogen: document.getElementById("nitrogen").value,
        phosphorus: document.getElementById("phosphorus").value,
        potassium: document.getElementById("potassium").value,
        ph: document.getElementById("ph").value,
        moisture: document.getElementById("moisture").value,
      };
      btn.disabled = true;
      btn.textContent = "Analyzing…";
      try {
        const result = await SmartCropAPI.analyzeSoil(body);
        renderResult(result);
      } catch (err) {
        alert.innerHTML = `<div class="alert alert-error">${err.message || "Analysis failed."}</div>`;
      } finally {
        btn.disabled = false;
        btn.textContent = "Analyze Soil";
      }
    });

    const imgForm = document.getElementById("soil-image-form");
    const imgBtn = document.getElementById("soil-img-btn");
    imgForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const fileInput = document.getElementById("soil-image");
      if (!fileInput.files.length) {
        document.getElementById("soil-alert").innerHTML = `<div class="alert alert-error">Please choose an image first.</div>`;
        return;
      }
      const fd = new FormData();
      fd.append("image", fileInput.files[0]);
      imgBtn.disabled = true;
      imgBtn.textContent = "Analyzing…";
      try {
        const result = await SmartCropAPI.uploadSoilImage(fd);
        renderImageResult(result);
      } catch (err) {
        document.getElementById("soil-alert").innerHTML = `<div class="alert alert-error">${err.message || "Could not analyze the photo."}</div>`;
      } finally {
        imgBtn.disabled = false;
        imgBtn.textContent = SmartCropI18n.t("soil.uploadBtn");
      }
    });
  });
})();
