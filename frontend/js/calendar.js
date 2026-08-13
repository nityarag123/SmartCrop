/* ============================================================
   SmartCrop — calendar.js (crop calendar)
   ============================================================ */

(function () {
  let currentData = null;

  function renderResult(data) {
    currentData = data;
    const el = document.getElementById("cal-result");
    const seasonSel = document.getElementById("cal-season");
    seasonSel.innerHTML = (data.seasons || []).map((s) =>
      `<option value="${s}" ${s === data.season ? "selected" : ""}>${s.charAt(0).toUpperCase() + s.slice(1)}</option>`).join("");

    const maxWeek = Math.max(...(data.phases || []).map((p) => p.week_end || 0), 1);
    el.innerHTML = `
      <div class="card" style="margin-bottom:16px;">
        <div class="flex-between">
          <h2>🌾 ${data.display_name} <span class="muted">· ${data.season.charAt(0).toUpperCase() + data.season.slice(1)}</span></h2>
          <span class="tag">${data.knowledge_base ? "knowledge base" : ""}</span>
        </div>
        <p class="muted">${data.soil || ""}</p>
      </div>
      <div class="timeline">
        ${(data.phases || []).map((p) => `
          <div class="tl-item">
            <div class="tl-rail">
              <span class="tl-dot"></span>
              <span class="tl-line" style="height:${Math.min(90, 40)}px;"></span>
            </div>
            <div class="tl-body card">
              <div class="flex-between">
                <b>${p.phase}</b>
                <span class="tag tag-soft">${p.week_start}–${p.week_end} wk</span>
              </div>
              <p class="muted">${p.activity}</p>
              <div class="tl-bar" style="width:${Math.min(100, Math.round((p.week_end / maxWeek) * 100))}%"></div>
            </div>
          </div>`).join("")}
      </div>`;
  }

  async function load(crop, season) {
    const alert = document.getElementById("cal-alert");
    alert.innerHTML = "";
    const el = document.getElementById("cal-result");
    el.innerHTML = `<span class="spinner"></span>`;
    try {
      const data = await SmartCropAPI.getCropCalendar(crop, season);
      renderResult(data);
    } catch (err) {
      el.innerHTML = "";
      alert.innerHTML = `<div class="alert alert-error">${err.message || "Could not load calendar."}</div>`;
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("cal-load").addEventListener("click", () => {
      load(document.getElementById("cal-crop").value, document.getElementById("cal-season").value);
    });
    document.getElementById("cal-season").addEventListener("change", () => {
      load(document.getElementById("cal-crop").value, document.getElementById("cal-season").value);
    });
    document.getElementById("cal-save").addEventListener("click", async () => {
      const alert = document.getElementById("cal-alert");
      try {
        const data = await SmartCropAPI.saveCropCalendar({
          crop: document.getElementById("cal-crop").value,
          season: document.getElementById("cal-season").value,
        });
        alert.innerHTML = `<div class="alert alert-success">${data.message || "Saved."}</div>`;
        document.getElementById("cal-status").textContent = "Saved as my crop for this season.";
      } catch (err) {
        alert.innerHTML = `<div class="alert alert-error">${err.message || "Could not save."}</div>`;
      }
    });
    load("rice", "kharif");
  });
})();
