/* ============================================================
   SmartCrop — weather.js
   ============================================================ */

(function () {
  let currentLocation = "";
  let currentCoords = null;

  function iconEmoji(icon) {
    const code = (icon || "").toLowerCase();
    if (code.includes("01")) return "☀️";
    if (code.includes("02")) return "🌤";
    if (code.includes("03") || code.includes("04")) return "☁️";
    if (code.includes("09") || code.includes("10")) return "🌧";
    if (code.includes("11")) return "⛈";
    if (code.includes("13")) return "🌨";
    if (code.includes("50")) return "🌫";
    return "🌡";
  }

  function renderCurrent(data) {
    const wrap = document.getElementById("weather-current");
    const c = data;
    const temp = c.temperature != null ? Math.round(c.temperature) : "—";
    const demo = c.demo ? `<span class="tag tag-warning" style="margin-left:8px;">demo data</span>` : `<span class="tag" style="margin-left:8px;">live</span>`;
    wrap.innerHTML = `
      <div class="card" style="margin-bottom:6px;">
        <div class="grid grid-2" style="align-items:center;">
          <div>
            <div class="eyebrow">📍 ${c.location || currentLocation}</div>
            <h2 style="font-size:3rem;margin:6px 0;">${iconEmoji(c.icon)} ${temp}°C</h2>
            <p class="muted">${c.condition} — ${c.description || ""}${demo}</p>
          </div>
          <div class="stat-row">
            <div class="stat"><span class="st-label">Feels like</span><b>${Math.round(c.feels_like || temp)}°C</b></div>
            <div class="stat"><span class="st-label">Humidity</span><b>${c.humidity != null ? c.humidity + "%" : "—"}</b></div>
            <div class="stat"><span class="st-label">Wind</span><b>${c.wind_speed != null ? c.wind_speed + " m/s" : "—"}</b></div>
            <div class="stat"><span class="st-label">Rain chance</span><b>${c.rain_probability != null ? c.rain_probability + "%" : "—"}</b></div>
          </div>
        </div>
      </div>`;
    wrap.classList.remove("hidden");
  }

  function renderForecast(days) {
    const grid = document.getElementById("weather-forecast");
    const tag = document.getElementById("forecast-tag");
    tag.textContent = (days && days[0] && days[0].demo) ? "demo data" : "live";
    if (!days || !days.length) { grid.innerHTML = `<p class="muted">No forecast available.</p>`; return; }
    grid.innerHTML = days.map((d) => `
      <div class="card" style="text-align:center;padding:16px 10px;">
        <div class="muted" style="font-size:.8rem;">${d.date || ""}</div>
        <div style="font-size:2rem;margin:6px 0;">${iconEmoji(d.icon)}</div>
        <div class="muted">${d.condition}</div>
        <b>${Math.round(d.temp_max)}° / ${Math.round(d.temp_min)}°</b>
        <div class="muted" style="font-size:.8rem;">Rain ${d.rain_probability}%${d.humidity != null ? " · " + d.humidity + "%" : ""}</div>
      </div>`).join("");
  }

  function renderAdvice(advice) {
    const el = document.getElementById("weather-advice");
    if (!advice || !advice.length) { el.innerHTML = `<span class="muted">No specific advice right now — follow your normal crop schedule.</span>`; return; }
    el.innerHTML = `<ul class="check-list">${advice.map((a) => `<li>${a}</li>`).join("")}</ul>`;
  }

  async function load(location, coords) {
    const loading = document.getElementById("weather-loading");
    const alert = document.getElementById("weather-alert");
    const input = document.getElementById("weather-location");
    loading.style.display = "block";
    alert.innerHTML = "";
    currentLocation = location;
    currentCoords = coords || null;
    if (input) input.value = location;
    try {
      const [current, forecast, adviceData] = await Promise.all([
        SmartCropAPI.getWeather(location, currentCoords),
        SmartCropAPI.getWeatherForecast(location, currentCoords),
        SmartCropAPI.getWeatherAdvice(location, currentCoords),
      ]);
      renderCurrent(current);
      renderForecast(forecast.days || []);
      renderAdvice(adviceData.advice || []);
    } catch (err) {
      alert.innerHTML = `<div class="alert alert-error">${err.message || "Could not load weather."}</div>`;
    } finally {
      loading.style.display = "none";
    }
  }

  async function getDefaultLocation() {
    // 1) Auto-detected location (GPS/IP) — the primary source
    const geo = SmartCropGeo.cached() || (await SmartCropGeo.detect());
    if (geo) {
      const label = geo.label || [geo.city, geo.state].filter(Boolean).join(", ");
      if (label) {
        currentCoords = geo.lat && geo.lng ? { lat: geo.lat, lng: geo.lng } : null;
        return { location: label, coords: currentCoords };
      }
    }
    // 2) Saved profile location
    try {
      const data = await SmartCropAPI.getProfile();
      if (data.user && data.user.location) return { location: data.user.location, coords: null };
    } catch (_) { /* not available */ }
    // 3) Sensible default
    return { location: "Pune, Maharashtra", coords: null };
  }

  function setDetecting(on) {
    const btn = document.getElementById("weather-geo");
    if (!btn) return;
    btn.disabled = on;
    btn.textContent = on ? "…" : "📍";
  }

  async function detectAndLoad() {
    setDetecting(true);
    const geo = await SmartCropGeo.detect();
    setDetecting(false);
    if (geo && (geo.label || geo.city)) {
      const label = geo.label || [geo.city, geo.state].filter(Boolean).join(", ");
      await load(label, (geo.lat && geo.lng) ? { lat: geo.lat, lng: geo.lng } : null);
      SmartCrop.toast("📍 Location detected: " + label, "success");
    } else {
      SmartCrop.toast("Could not detect your location. Please type it.", "warning");
    }
  }

  document.addEventListener("DOMContentLoaded", async () => {
    const input = document.getElementById("weather-location");
    document.getElementById("weather-search").addEventListener("submit", (e) => {
      e.preventDefault();
      const value = input.value.trim();
      if (value) load(value, null);
    });
    const geoBtn = document.getElementById("weather-geo");
    if (geoBtn) geoBtn.addEventListener("click", detectAndLoad);

    const def = await getDefaultLocation();
    load(def.location, def.coords);
  });
})();
