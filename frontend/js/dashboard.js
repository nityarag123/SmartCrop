/* ============================================================
   SmartCrop — dashboard.js
   ============================================================ */

(function () {
  function renderWeatherMini(data) {
    const el = document.getElementById("dash-weather");
    if (!el) return;
    if (!data || data.error || typeof data.temperature !== "number") {
      el.textContent = "🌤 Weather service demo";
      return;
    }
    const temp = Math.round(data.temperature);
    el.innerHTML = `<b>${temp}°C</b> ${data.condition || ""} · ${data.location || ""} <span class="muted">${data.demo ? "· demo data" : "· live"}</span>`;
  }

  function renderRecent(data) {
    const body = document.getElementById("dash-recent-body");
    if (!body) return;
    const notifications = data.notifications || [];
    if (!notifications.length) {
      body.innerHTML = `<div class="state-box"><span class="sb-ico">🌱</span>No activity yet. Try the AI tools to get started!</div>`;
      return;
    }
    body.innerHTML = notifications.map((n, i) => `
      <div class="recent-row">
        <span class="rr-ico">${n.icon || "✅"}</span>
        <div class="rr-text"><b>${n.text || n.title || ""}</b><span>${n.detail || ""}</span></div>
        <span class="rr-time">${n.created_at ? n.created_at.split("T")[0] : ""}</span>
      </div>`).join("");
  }

  async function load() {
    // Pass auto-detected coordinates so weather works even without a saved profile location.
    let coords = null;
    const geo = SmartCropGeo.cached() || (await SmartCropGeo.detect());
    if (geo && typeof geo.lat === "number" && typeof geo.lng === "number") {
      coords = { lat: geo.lat, lng: geo.lng };
    }
    try {
      const data = await SmartCropAPI.getDashboard(coords);
      if (data.weather) renderWeatherMini(data.weather);
      renderRecent(data);
    } catch (err) {
      const w = document.getElementById("dash-weather");
      if (w) w.textContent = "⚠ " + (err.message || "Error");
      const body = document.getElementById("dash-recent-body");
      if (body) body.innerHTML = `<div class="state-box">${err.message || "Could not load dashboard."}</div>`;
    }
  }

  document.addEventListener("DOMContentLoaded", load);
})();
