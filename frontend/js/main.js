/* ============================================================
   SmartCrop — main.js
   Renders the shared header / footer / mobile navigation,
   handles login state, language selection, toasts and auth guard.
   ============================================================ */

(function () {
  const NAV_ITEMS = [
    { key: "nav.home", label: "nav.home", href: "index.html", ico: "🏠" },
    { key: "nav.dashboard", label: "nav.dashboard", href: "dashboard.html", ico: "📊" },
    { key: "nav.weather", label: "nav.weather", href: "weather.html", ico: "🌦" },
    { key: "nav.crop", label: "nav.crop", href: "crop-recommendation.html", ico: "🌱" },
    { key: "nav.soil", label: "nav.soil", href: "soil.html", ico: "🧪" },
    { key: "nav.pest", label: "nav.pest", href: "pest-detection.html", ico: "🐛" },
    { key: "nav.calendar", label: "nav.calendar", href: "crop-calendar.html", ico: "📅" },
    { key: "nav.schemes", label: "nav.schemes", href: "schemes.html", ico: "🏛" },
    { key: "nav.chat", label: "nav.chat", href: "chatbot.html", ico: "🤖" },
    { key: "nav.profile", label: "nav.profile", href: "profile.html", ico: "👤" },
  ];

  const MOBILE_NAV = [
    { label: "nav.dashboard", href: "dashboard.html", ico: "📊" },
    { label: "nav.crop", href: "crop-recommendation.html", ico: "🌱" },
    { label: "nav.weather", href: "weather.html", ico: "🌦" },
    { label: "nav.chat", href: "chatbot.html", ico: "🤖" },
    { label: "nav.more", href: "javascript:void(0)", ico: "☰", more: true },
  ];

  let user = null;

  function currentPage() {
    const name = (location.pathname.split("/").pop() || "index.html").toLowerCase();
    return name;
  }

  function isActive(href) {
    return currentPage() === href.toLowerCase();
  }

  function langSelector() {
    const select = document.createElement("select");
    select.className = "lang-select";
    select.setAttribute("aria-label", SmartCropI18n.t("common.language"));
    [["en", "English"], ["hi", "हिन्दी"], ["te", "తెలుగు"], ["ta", "தமிழ்"], ["gu", "ગુજરાતી"]]
      .forEach(([code, name]) => {
        const opt = document.createElement("option");
        opt.value = code;
        opt.textContent = name;
        select.appendChild(opt);
      });
    select.value = SmartCropI18n.lang;
    select.addEventListener("change", () => SmartCropI18n.setLang(select.value));
    return select;
  }

  function renderHeader() {
    const header = document.getElementById("site-header");
    if (!header) return;

    const menuLinks = NAV_ITEMS.map((item) =>
      `<a class="menu-item" href="${item.href}"><span class="mi-ico">${item.ico}</span><span data-i18n="${item.label}"></span></a>`
    ).join("");

    header.innerHTML = `
      <div class="container header-inner">
        <a class="brand" href="index.html">
          <img src="assets/icons/logo.svg" alt="SmartCrop logo">
          <span class="text">${SmartCropI18n.t("app.name")}</span>
        </a>
        <nav class="main-nav" aria-label="Main navigation">
          ${NAV_ITEMS.slice(0, 5).map((item) =>
            `<a href="${item.href}" class="${isActive(item.href) ? "active" : ""}" data-i18n="${item.label}"></a>`
          ).join("")}
          <a href="javascript:void(0)" id="nav-more-btn" class="js-nav-more">${SmartCropI18n.t("nav.more")}</a>
        </nav>
        <div class="header-actions">
          <div id="lang-slot"></div>
          <button class="icon-btn" id="notif-btn" title="Notifications" aria-label="Notifications">🔔<span class="badge hidden" id="notif-badge">0</span></button>
          <a class="icon-btn" href="profile.html" title="Profile" aria-label="Profile">👤</a>
          <button class="icon-btn nav-toggle" id="nav-toggle" aria-label="Menu">☰</button>
        </div>
      </div>
      <div class="menu-overlay" id="menu-overlay">
        <div class="menu-panel">
          <div class="menu-head">
            <strong>${SmartCropI18n.t("app.name")}</strong>
            <button class="icon-btn" id="menu-close">✕</button>
          </div>
          ${menuLinks}
          <div class="mt-3" id="menu-auth-actions"></div>
        </div>
      </div>`;

    const langSlot = document.getElementById("lang-slot");
    langSlot.appendChild(langSelector());

    document.getElementById("nav-toggle").addEventListener("click", () => openMenu());
    document.getElementById("nav-more-btn").addEventListener("click", (e) => { e.preventDefault(); openMenu(); });
    document.getElementById("menu-close").addEventListener("click", () => closeMenu());
    document.getElementById("menu-overlay").addEventListener("click", (e) => {
      if (e.target.id === "menu-overlay") closeMenu();
    });
    document.getElementById("notif-btn").addEventListener("click", () => {
      window.SmartCrop.showNotifications();
    });

    // Re-render the header on language change
    window.SmartCropOnLangChange = () => renderHeader();
  }

  function openMenu() { document.getElementById("menu-overlay").classList.add("open"); }
  function closeMenu() { document.getElementById("menu-overlay").classList.remove("open"); }

  function renderMobileNav() {
    const wrap = document.getElementById("mobile-nav");
    if (!wrap) return;
    wrap.innerHTML = MOBILE_NAV.map((item) => {
      if (item.more) {
        return `<a href="javascript:void(0)" id="mnav-more"><span class="mnav-ico">${item.ico}</span><span data-i18n="${item.label}"></span></a>`;
      }
      const active = isActive(item.href) ? "active" : "";
      return `<a href="${item.href}" class="${active}"><span class="mnav-ico">${item.ico}</span><span data-i18n="${item.label}"></span></a>`;
    }).join("");
    const moreBtn = document.getElementById("mnav-more");
    if (moreBtn) moreBtn.addEventListener("click", () => openMenu());
  }

  function renderFooter() {
    const footer = document.getElementById("site-footer");
    if (!footer) return;
    footer.innerHTML = `
      <div class="container">
        <div class="footer-grid">
          <div>
            <h4>${SmartCropI18n.t("app.name")}</h4>
            <p class="small">${SmartCropI18n.t("footer.about")}</p>
          </div>
          <div>
            <h4>${SmartCropI18n.t("footer.quickLinks")}</h4>
            <p class="small">
              <a href="weather.html" data-i18n="nav.weather"></a> ·
              <a href="crop-recommendation.html" data-i18n="nav.crop"></a> ·
              <a href="soil.html" data-i18n="nav.soil"></a> ·
              <a href="pest-detection.html" data-i18n="nav.pest"></a> ·
              <a href="schemes.html" data-i18n="nav.schemes"></a>
            </p>
          </div>
          <div>
            <h4>${SmartCropI18n.t("footer.contact")}</h4>
            <p class="small">📞 Helpline (Kisan Call Centre): 1800-180-1551<br>✉️ support@smartcrop.example</p>
          </div>
        </div>
        <p class="foot-note">${SmartCropI18n.t("footer.rights")}</p>
      </div>`;
  }

  async function loadUser() {
    try {
      const data = await SmartCropAPI.authStatus();
      if (data.logged_in) user = data.user;
    } catch (_) { user = null; }
    const logoutLinks = document.querySelectorAll("[data-action=logout]");
    logoutLinks.forEach((link) => {
      link.addEventListener("click", async (e) => {
        e.preventDefault();
        await SmartCropAPI.logout();
        location.href = "index.html";
      });
    });
  }

  async function guard() {
    const required = document.body.getAttribute("data-auth") === "required";
    const optional = document.body.getAttribute("data-auth") === "optional";
    try {
      const data = await SmartCropAPI.authStatus();
      if (data.logged_in) user = data.user;
    } catch (_) { user = null; }
    if (required && !user) {
      location.href = "login.html?next=" + encodeURIComponent(location.pathname.split("/").pop());
      return;
    }
    if (user) {
      const authLinks = document.querySelectorAll("[data-auth-view]");
      authLinks.forEach((el) => {
        if (el.getAttribute("data-auth-view") === "guest") el.classList.add("hidden");
      });
      const nameEl = document.getElementById("user-name");
      if (nameEl) nameEl.textContent = user.name || user.email;
      const locEl = document.getElementById("user-location");
      if (locEl) {
        if (user.location) {
          locEl.textContent = "📍 " + user.location;
        } else if (window.SmartCropGeo) {
          const cached = SmartCropGeo.cached();
          if (cached && cached.label) locEl.textContent = "📍 " + cached.label;
          SmartCropGeo.detect().then((geo) => {
            if (geo && geo.label && locEl && !locEl.textContent) locEl.textContent = "📍 " + geo.label;
          });
        }
      }
      const langSelect = document.querySelector(".lang-select");
      if (langSelect && user.language && SmartCropI18n.data[user.language]) {
        langSelect.value = user.language;
        SmartCropI18n.setLang(user.language);
      }
    }
  }

  function renderUserMenuAuth() {
    const slot = document.getElementById("menu-auth-actions");
    if (!slot) return;
    if (user) {
      slot.innerHTML = `<a class="menu-item" href="javascript:void(0)" data-action="logout"><span class="mi-ico">🚪</span><span>${SmartCropI18n.t("nav.logout")}</span></a>`;
    } else {
      slot.innerHTML = `
        <a class="menu-item" href="login.html"><span class="mi-ico">🔑</span><span>${SmartCropI18n.t("nav.login")}</span></a>
        <a class="menu-item" href="register.html"><span class="mi-ico">📝</span><span>${SmartCropI18n.t("nav.register")}</span></a>`;
    }
  }

  async function boot() {
    renderHeader();
    renderMobileNav();
    renderFooter();
    await guard();
    renderUserMenuAuth();
    SmartCropI18n.apply();
  }

  document.addEventListener("DOMContentLoaded", boot);

  /* ------- Toast helper ------- */
  function toast(message, type = "success") {
    let wrap = document.querySelector(".toast-wrap");
    if (!wrap) {
      wrap = document.createElement("div");
      wrap.className = "toast-wrap";
      document.body.appendChild(wrap);
    }
    const el = document.createElement("div");
    el.className = "toast " + (type === "error" ? "error" : type === "warning" ? "warning" : "");
    el.textContent = message;
    wrap.appendChild(el);
    setTimeout(() => el.remove(), 3800);
  }

  /* ------- Notifications panel ------- */
  function showNotifications() {
    const panel = document.createElement("div");
    panel.className = "menu-overlay open";
    panel.innerHTML = `
      <div class="menu-panel">
        <div class="menu-head"><strong>${SmartCropI18n.t("nav.notifications") || "Notifications"}</strong>
          <button class="icon-btn" id="n-close">✕</button></div>
        <div id="n-body"><div class="spinner"></div></div>
      </div>`;
    document.body.appendChild(panel);
    panel.querySelector("#n-close").addEventListener("click", () => panel.remove());
    panel.addEventListener("click", (e) => { if (e.target === panel) panel.remove(); });

    (async () => {
      try {
        const data = await SmartCropAPI.getDashboard();
        const items = data.notifications || [];
        const body = panel.querySelector("#n-body");
        if (!items.length) {
          body.innerHTML = `<div class="state-box"><span class="sb-ico">✅</span>All caught up!</div>`;
        } else {
          body.innerHTML = items.map((n) => `<div class="card" style="margin-bottom:10px;padding:14px;">${n.icon} ${n.text}</div>`).join("");
        }
      } catch (_) {
        panel.querySelector("#n-body").innerHTML = `<div class="state-box">${SmartCropI18n.t("common.error")}</div>`;
      }
    })();
  }

  window.SmartCrop = { toast, showNotifications, get user() { return user; } };
})();
