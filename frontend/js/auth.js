/* ============================================================
   SmartCrop — auth page logic (login.html / register.html)
   ============================================================ */

(function () {
  function showAlert(message, type = "error") {
    const box = document.getElementById("auth-alert");
    if (!box) return;
    box.innerHTML = `<div class="alert ${type === "error" ? "alert-error" : "alert-success"}">${message}</div>`;
  }

  function togglePassword(btnId) {
    const btn = document.getElementById(btnId);
    if (!btn) return;
    btn.addEventListener("click", () => {
      const input = btn.previousElementSibling;
      if (!input) return;
      const isPassword = input.type === "password";
      input.type = isPassword ? "text" : "password";
      btn.textContent = isPassword ? "🙈" : "👁";
    });
  }

  function setupLangPicker() {
    const picker = document.getElementById("lang-picker");
    if (!picker) return;
    const buttons = picker.querySelectorAll("button");
    const current = SmartCropI18n.lang;
    buttons.forEach((b) => {
      if (b.dataset.lang === current) b.classList.add("selected");
      b.addEventListener("click", () => {
        buttons.forEach((x) => x.classList.remove("selected"));
        b.classList.add("selected");
        SmartCropI18n.setLang(b.dataset.lang);
      });
    });
  }

  async function handleLogin(e) {
    e.preventDefault();
    const btn = document.getElementById("login-btn");
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (!email || !password) {
      showAlert("Please enter both email and password.");
      return;
    }
    btn.disabled = true;
    btn.textContent = "Logging in...";
    try {
      const data = await SmartCropAPI.login({ email, password });
      if (data.logged_in || data.user) {
        showAlert("Login successful! Redirecting...", "success");
        const next = new URLSearchParams(location.search).get("next");
        setTimeout(() => location.assign(next && !next.includes("login") ? next : "dashboard.html"), 700);
      } else {
        showAlert(data.message || "Invalid email or password.");
      }
    } catch (err) {
      showAlert(err.message || "Could not connect to the server. Is the backend running?");
    } finally {
      btn.disabled = false;
      btn.textContent = SmartCropI18n.t("nav.login");
    }
  }

  async function handleRegister(e) {
    e.preventDefault();
    const btn = document.getElementById("register-btn");
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const selectedLang = document.querySelector("#lang-picker button.selected");
    const language = selectedLang ? selectedLang.dataset.lang : "en";

    if (!name || !email || !password) {
      showAlert("Please fill in your name, email and password.");
      return;
    }
    if (password.length < 6) {
      showAlert("Password must be at least 6 characters long.");
      return;
    }
    btn.disabled = true;
    btn.textContent = "Creating account...";
    try {
      const data = await SmartCropAPI.register({ name, email, password, language });
      if (data.created || data.user) {
        showAlert("Account created! Redirecting...", "success");
        setTimeout(() => location.assign("dashboard.html"), 800);
      } else {
        showAlert(data.message || "Registration failed. Please try again.");
      }
    } catch (err) {
      showAlert(err.message || "Could not connect to the server. Is the backend running?");
    } finally {
      btn.disabled = false;
      btn.textContent = SmartCropI18n.t("auth.registerBtn");
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("login-form");
    const regForm = document.getElementById("register-form");
    if (form) form.addEventListener("submit", handleLogin);
    if (regForm) regForm.addEventListener("submit", handleRegister);
    togglePassword("toggle-pass");
    setupLangPicker();
  });
})();
