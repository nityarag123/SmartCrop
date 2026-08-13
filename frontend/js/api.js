/* ============================================================
   SmartCrop — central API service
   All fetch() calls go through here. No duplicate fetch logic.
   ============================================================ */

const SmartCropAPI = (() => {
  const BASE = "";

  async function request(path, options = {}) {
    const { body, formData, headers = {}, timeout = 30000 } = options;
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeout);

    const init = {
      method: options.method || (body || formData ? "POST" : "GET"),
      headers: { ...headers },
      credentials: "same-origin",
      signal: controller.signal,
    };

    if (formData) {
      init.body = formData; // let the browser set the multipart boundary
    } else if (body) {
      init.headers["Content-Type"] = "application/json";
      init.body = JSON.stringify(body);
    }

    try {
      const response = await fetch(BASE + path, init);
      let data = null;
      const text = await response.text();
      try { data = text ? JSON.parse(text) : {}; } catch (_) { data = { error: text }; }
      if (!response.ok) {
        const err = new Error((data && data.error) || `Request failed (${response.status})`);
        err.status = response.status;
        err.data = data;
        throw err;
      }
      return data;
    } catch (error) {
      if (error.name === "AbortError") {
        throw new Error("The request took too long. Please try again.");
      }
      throw error;
    } finally {
      clearTimeout(timer);
    }
  }

  /* ------- Auth ------- */
  const register = (data) => request("/api/auth/register", { body: data });
  const login = (data) => request("/api/auth/login", { body: data });
  const logout = () => request("/api/auth/logout", { method: "POST" });
  const me = () => request("/api/auth/me");
  const authStatus = () => request("/api/auth/status");

  /* ------- Profile ------- */
  const getProfile = () => request("/api/profile");
  const updateProfile = (data) => request("/api/profile", { method: "PUT", body: data });

  /* ------- Weather ------- */
  function weatherQuery(location, coords) {
    const params = new URLSearchParams();
    if (location) params.set("location", location);
    if (coords && typeof coords.lat === "number" && typeof coords.lng === "number") {
      params.set("lat", coords.lat.toFixed(5));
      params.set("lon", coords.lng.toFixed(5));
    }
    return params.toString();
  }
  const getWeather = (location, coords) => request(`/api/weather?${weatherQuery(location, coords)}`);
  const getWeatherForecast = (location, coords) => request(`/api/weather/forecast?${weatherQuery(location, coords)}`);
  const getWeatherAdvice = (location, coords) => request(`/api/weather/advice?${weatherQuery(location, coords)}`);

  /* ------- Crop recommendation ------- */
  const recommendCrop = (data) => request("/api/crop/recommend", { body: data });

  /* ------- Soil analysis ------- */
  const analyzeSoil = (data) => request("/api/soil/analyze", { body: data });
  const uploadSoilImage = (formData) => request("/api/soil/image", { formData });

  /* ------- Pest detection ------- */
  const detectPest = (formData) => request("/api/pest/detect", { formData, timeout: 60000 });

  /* ------- Chat ------- */
  const sendChatMessage = (data) => request("/api/chat", { body: data, timeout: 60000 });
  const getChatHistory = () => request("/api/chat/history");

  /* ------- Calendar ------- */
  const getCropCalendar = (crop, season) =>
    request(`/api/calendar?crop=${encodeURIComponent(crop || "")}&season=${encodeURIComponent(season || "")}`);
  const saveCropCalendar = (data) => request("/api/calendar", { body: data });

  /* ------- Schemes ------- */
  const getSchemes = (filters = {}) => {
    const qs = new URLSearchParams(
      Object.entries(filters).filter(([, v]) => v)
    ).toString();
    return request(`/api/schemes${qs ? "?" + qs : ""}`);
  };

  /* ------- Dashboard ------- */
  const getDashboard = (coords) => {
    const qs = new URLSearchParams();
    if (coords && typeof coords.lat === "number" && typeof coords.lng === "number") {
      qs.set("lat", coords.lat.toFixed(5));
      qs.set("lon", coords.lng.toFixed(5));
    }
    const q = qs.toString();
    return request(`/api/dashboard${q ? "?" + q : ""}`);
  };

  return {
    register, login, logout, me, authStatus,
    getProfile, updateProfile,
    getWeather, getWeatherForecast, getWeatherAdvice,
    recommendCrop, analyzeSoil, uploadSoilImage, detectPest,
    sendChatMessage, getChatHistory,
    getCropCalendar, saveCropCalendar,
    getSchemes, getDashboard,
  };
})();
