/* ============================================================
   SmartCrop — crop.js (crop recommendation)
   ============================================================ */

(function () {
  function renderResult(r) {
    const el = document.getElementById("crop-result");
    const engineTag = r.engine === "ML"
      ? `<span class="tag">ML model</span>`
      : `<span class="tag tag-warning">rule-based</span>`;
    el.innerHTML = `
      <div class="card" style="margin-bottom:16px;border:2px solid var(--green-300);">
        <div class="flex-between"><h3 data-i18n="crop.result">Recommended crop</h3>${engineTag}</div>
        <h1 style="font-size:2.6rem;color:var(--green-700);margin:8px 0;">🌾 ${r.crop}</h1>
        <p class="muted">${r.reason}</p>
        <div class="confidence-box">
          <div class="conf-label">Confidence</div>
          <div class="conf-track"><div class="conf-fill" style="width:${Math.max(5, Math.min(100, r.confidence || 0))}%">${r.confidence}%</div></div>
        </div>
      </div>

      <div class="card" style="margin-bottom:16px;">
        <h3 data-i18n="crop.alt">Other suitable crops</h3>
        <div class="chip-row">
          ${(r.alternatives || []).map((a) => `<span class="stat-pill">🌱 ${a.crop} <small>(${a.confidence}%)</small></span>`).join("") || `<span class="muted">—</span>`}
        </div>
      </div>

      <div class="grid grid-2" style="gap:16px;">
        <div class="card"><h3>💧 <span data-i18n="crop.water">Water requirement</span></h3><p>${r.water_requirement || "—"}</p></div>
        <div class="card"><h3>🗓 <span data-i18n="crop.season">Growing season</span></h3><p>${r.growing_season || "—"}</p></div>
      </div>

      <div class="grid grid-2" style="gap:16px;margin-top:16px;">
        <div class="card"><h3>🪨 <span data-i18n="crop.soil">Suitable soil</span></h3><p>${r.suitable_soil || "—"}</p></div>
        <div class="card"><h3>🧑‍🌾 <span data-i18n="crop.guidance">Growing guidance</span></h3><p>${r.guidance || "—"}</p></div>
      </div>

      <div class="card" style="margin-top:16px;background:var(--green-50);">
        <p class="muted small">🌡 ${r.inputs.temperature}°C · 💨 ${r.inputs.humidity}% · 🌧 ${r.inputs.rainfall}mm · pH ${r.inputs.ph} · N ${r.inputs.nitrogen} · P ${r.inputs.phosphorus} · K ${r.inputs.potassium}</p>
      </div>`;
    el.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  async function fillFromLocation(btn) {
    const original = btn.textContent;
    btn.disabled = true;
    btn.textContent = "Detecting…";
    const geo = await SmartCropGeo.detect();
    btn.disabled = false;
    btn.textContent = original;
    const alert = document.getElementById("crop-alert");
    if (!geo || !(geo.label || geo.city)) {
      alert.innerHTML = `<div class="alert alert-warning">Could not detect your location. Please enter the values manually.</div>`;
      return;
    }
    const label = geo.label || [geo.city, geo.state].filter(Boolean).join(", ");
    const coords = (geo.lat && geo.lng) ? { lat: geo.lat, lng: geo.lng } : null;
    try {
      const w = await SmartCropAPI.getWeather(label, coords);
      const set = (id, value) => { const el = document.getElementById(id); if (el && value != null) el.value = value; };
      set("temperature", w.temperature != null ? Math.round(w.temperature) : null);
      set("humidity", w.humidity != null ? Math.round(w.humidity) : null);
      set("rainfall", w.rainfall != null ? Math.round(w.rainfall) : null);
      const filled = ["temperature", "humidity", "rainfall"].some((id) => document.getElementById(id).value);
      if (SmartCrop.toast) SmartCrop.toast("📍 " + label + " — weather fields filled", "success");
      else alert.innerHTML = `<div class="alert alert-success">📍 Location detected: ${label} — weather fields filled.</div>`;
    } catch (err) {
      alert.innerHTML = `<div class="alert alert-error">${err.message || "Could not fetch weather for your location."}</div>`;
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    const geoBtn = document.getElementById("crop-geo");
    if (geoBtn) geoBtn.addEventListener("click", () => fillFromLocation(geoBtn));
    document.getElementById("crop-form").addEventListener("submit", async (e) => {
      e.preventDefault();
      const alert = document.getElementById("crop-alert");
      alert.innerHTML = "";
      const ids = ["temperature", "humidity", "rainfall", "ph", "nitrogen", "phosphorus", "potassium"];
      const body = {};
      ids.forEach((id) => { body[id] = document.getElementById(id).value; });
      const btn = document.getElementById("crop-btn");
      btn.disabled = true;
      btn.textContent = "Analyzing…";
      try {
        const result = await SmartCropAPI.recommendCrop(body);
        renderResult(result);
      } catch (err) {
        alert.innerHTML = `<div class="alert alert-error">${err.message || "Recommendation failed."}</div>`;
      } finally {
        btn.disabled = false;
        btn.textContent = "Recommend Crop";
      }
    });
  });
})();
