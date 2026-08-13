/* ============================================================
   SmartCrop — geo.js
   Automatic location detection:
     1. Browser geolocation (GPS / network) with the user's permission
     2. Reverse-geocoding to village/city + state (BigDataCloud, free, no key)
     3. IP-based fallback when the browser can't give a position
   Results are cached in localStorage as "smartcrop.geo".
   ============================================================ */

const SmartCropGeo = (() => {
  const REVERSE_URL = "https://api.bigdatacloud.net/data/reverse-geocode-client";
  const IP_PROVIDERS = [
    { url: "https://ipwho.is/", lat: "latitude", lng: "longitude" },
    { url: "https://get.geojs.io/v1/ip/geo.json", lat: "latitude", lng: "longitude" },
    { url: "https://api.bigdatacloud.net/data/ip-geolocation-with-confidence?localityLanguage=en", lat: "latitude", lng: "longitude" },
  ];

  function fromBrowser() {
    if (!("geolocation" in navigator)) return Promise.resolve(null);
    return new Promise((resolve) => {
      navigator.geolocation.getCurrentPosition(
        (pos) => resolve({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
        () => resolve(null),
        { timeout: 8000, maximumAge: 15 * 60 * 1000 }
      );
    });
  }

  async function fromIP() {
    for (const provider of IP_PROVIDERS) {
      try {
        const response = await fetch(provider.url);
        if (!response.ok) continue;
        const data = await response.json();
        const lat = Number(data[provider.lat]);
        const lng = Number(data[provider.lng]);
        if (Number.isFinite(lat) && Number.isFinite(lng)) {
          return { lat, lng };
        }
      } catch (_) { /* offline / blocked — try next provider */ }
    }
    return null;
  }

  async function reverseGeocode(lat, lng) {
    const fallback = {
      lat, lng,
      city: "",
      district: "",
      state: "",
      country: "",
      label: `${lat.toFixed(2)}, ${lng.toFixed(2)}`,
    };
    try {
      const response = await fetch(
        `${REVERSE_URL}?latitude=${lat}&longitude=${lng}&localityLanguage=en`
      );
      if (!response.ok) return fallback;
      const data = await response.json();
      const locality = data.locality || data.city || data.principalSubdivision || "";
      const state = data.principalSubdivision || "";
      const city = data.city || data.locality || "";
      const label = [locality || city, state, data.countryName].filter(Boolean).join(", ") ||
                    fallback.label;
      return {
        lat, lng,
        city,
        district: locality || city,
        state,
        country: data.countryName || "",
        label,
      };
    } catch (_) {
      return fallback;
    }
  }

  function cached() {
    try {
      const raw = localStorage.getItem("smartcrop.geo");
      if (raw) {
        const parsed = JSON.parse(raw);
        if (parsed && (parsed.lat || parsed.label)) return parsed;
      }
    } catch (_) { /* ignore */ }
    return null;
  }

  async function detect() {
    // Fast path: already detected before (max age respected by geolocation call below)
    const coords = (await fromBrowser()) || (await fromIP());
    if (!coords) return cached();
    const place = await reverseGeocode(coords.lat, coords.lng);
    try { localStorage.setItem("smartcrop.geo", JSON.stringify(place)); } catch (_) { /* ignore */ }
    return place;
  }

  return { detect, cached };
})();
