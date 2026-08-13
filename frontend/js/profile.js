/* ============================================================
   SmartCrop — profile.js
   ============================================================ */

(function () {
  async function load() {
    const loading = document.getElementById("profile-loading");
    const form = document.getElementById("profile-form");
    const alert = document.getElementById("profile-alert");
    try {
      const data = await SmartCropAPI.getProfile();
      const u = data.user || {};
      document.getElementById("p-name").value = u.name || "";
      document.getElementById("p-phone").value = u.phone || "";
      document.getElementById("p-email").value = u.email || "";
      document.getElementById("p-location").value = u.location || "";
      document.getElementById("p-state").value = u.state || "";
      document.getElementById("p-district").value = u.district || "";
      document.getElementById("p-farm-size").value = u.farm_size || "";
      document.getElementById("p-crop").value = u.current_crop || "";
      document.getElementById("p-soil-info").value = u.soil_info || "";
      document.getElementById("p-irrigation").value = u.irrigation || "";
      const langSel = document.getElementById("p-language");
      if (langSel && u.language) langSel.value = u.language;
      form.classList.remove("hidden");
    } catch (err) {
      alert.innerHTML = `<div class="alert alert-error">${err.message || "Could not load your profile."}</div>`;
    } finally {
      loading.style.display = "none";
    }
  }

  function setupLocationDetect() {
    const btn = document.getElementById("loc-detect");
    if (!btn) return;
    btn.addEventListener("click", async () => {
      btn.disabled = true;
      btn.textContent = "Detecting…";
      const geo = await SmartCropGeo.detect();
      btn.disabled = false;
      btn.textContent = SmartCropI18n.t("auth.detectLocation");
      if (!geo || !(geo.label || geo.city)) {
        document.getElementById("profile-alert").innerHTML = `<div class="alert alert-warning">Could not detect your location. Please enter it manually.</div>`;
        return;
      }
      const label = geo.label || [geo.city, geo.state].filter(Boolean).join(", ");
      const loc = document.getElementById("p-location");
      if (loc) loc.value = label;
      if (geo.state) document.getElementById("p-state").value = geo.state;
      if (geo.district) document.getElementById("p-district").value = geo.district;
      document.getElementById("profile-alert").innerHTML = `<div class="alert alert-success">📍 Location detected: ${label}</div>`;
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    load();
    setupLocationDetect();
    document.getElementById("profile-form").addEventListener("submit", async (e) => {
      e.preventDefault();
      const alert = document.getElementById("profile-alert");
      alert.innerHTML = "";
      const body = {
        name: document.getElementById("p-name").value.trim(),
        phone: document.getElementById("p-phone").value.trim(),
        location: document.getElementById("p-location").value.trim(),
        state: document.getElementById("p-state").value.trim(),
        district: document.getElementById("p-district").value.trim(),
        language: document.getElementById("p-language").value,
        farm_size: document.getElementById("p-farm-size").value.trim(),
        current_crop: document.getElementById("p-crop").value.trim(),
        soil_info: document.getElementById("p-soil-info").value.trim(),
        irrigation: document.getElementById("p-irrigation").value,
      };
      const btn = document.getElementById("profile-save");
      btn.disabled = true;
      btn.textContent = "Saving…";
      try {
        const data = await SmartCropAPI.updateProfile(body);
        alert.innerHTML = `<div class="alert alert-success">${data.message || "Saved successfully."}</div>`;
        if (data.user && data.user.language) SmartCropI18n.setLang(data.user.language);
      } catch (err) {
        alert.innerHTML = `<div class="alert alert-error">${err.message || "Could not save your profile."}</div>`;
      } finally {
        btn.disabled = false;
        btn.textContent = "Save";
      }
    });
  });
})();
