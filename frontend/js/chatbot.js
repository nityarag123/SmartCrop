/* ============================================================
   SmartCrop — chatbot.js
   ============================================================ */

(function () {
  const messagesEl = document.getElementById("chat-messages");
  const inputEl = document.getElementById("chat-input");
  const sendBtn = document.getElementById("chat-send");
  const listenBtn = document.getElementById("listen-toggle");
  const speakBtn = document.getElementById("speak-toggle");

  let ttsOn = false;
  let historyLoaded = false;
  const SUGGESTIONS = [
    "What is the best crop for this season?",
    "How do I treat aphids?",
    "What is PM-KISAN?",
    "Best fertiliser for paddy",
    "Current market price of wheat",
    "Symptoms of nitrogen deficiency",
  ];

  function scrollBottom() { messagesEl.scrollTop = messagesEl.scrollHeight; }

  function addMessage(text, who) {
    const div = document.createElement("div");
    div.className = "chat-msg " + who;
    div.textContent = text;
    messagesEl.appendChild(div);
    scrollBottom();
    return div;
  }

  function showTyping() {
    const div = document.createElement("div");
    div.className = "chat-typing";
    div.innerHTML = "<i></i><i></i><i></i>";
    div.id = "typing-indicator";
    messagesEl.appendChild(div);
    scrollBottom();
  }

  function hideTyping() {
    const t = document.getElementById("typing-indicator");
    if (t) t.remove();
  }

  function renderSuggestions() {
    const wrap = document.getElementById("chat-suggestions");
    if (!wrap) return;
    wrap.innerHTML = SUGGESTIONS.map((s, i) =>
      `<button type="button" data-s="${i}">${s}</button>`).join("");
    wrap.querySelectorAll("button").forEach((b) => {
      b.addEventListener("click", () => {
        inputEl.value = b.textContent;
        send();
      });
    });
  }

  async function send() {
    const text = inputEl.value.trim();
    if (!text) return;
    inputEl.value = "";
    addMessage(text, "user");
    showTyping();
    try {
      const data = await SmartCropAPI.sendChatMessage({ message: text, lang: SmartCropI18n.lang });
      hideTyping();
      const reply = data.response || "I could not understand that. Please try again.";
      addMessage(reply, "bot");
      if (ttsOn) SmartCropVoice.speak(reply.replace(/[*#>`]/g, ""), SmartCropI18n.lang);
    } catch (err) {
      hideTyping();
      addMessage("⚠ " + (err.message || "Could not reach the assistant."), "bot");
    }
  }

  async function loadHistory() {
    try {
      const data = await SmartCropAPI.getChatHistory();
      const messages = data.messages || [];
      if (messages.length) {
        messagesEl.innerHTML = "";
        messages.forEach((m) => {
          if (m.message) addMessage(m.message, "user");
          if (m.response) addMessage(m.response, "bot");
        });
        historyLoaded = true;
      }
    } catch (_) { /* history optional */ }
    if (!historyLoaded && !messagesEl.children.length) {
      addMessage("🙏 Namaste! I am SmartCrop, your AI farm assistant.\nAsk me anything about crops, soil, pests, weather or government schemes. You can also press the 🎤 button and speak.", "bot");
    }
  }

  function toggleListening() {
    if (!SmartCropVoice.speechSupported()) {
      addMessage("⚠ Speech recognition is not supported in this browser. Please type your question instead.", "bot");
      return;
    }
    if (listening) {
      SmartCropVoice.stopRecognition();
      setListening(false);
      return;
    }
    SmartCropVoice.startRecognition({
      lang: SmartCropI18n.lang,
      onResult: (transcript) => {
        setListening(false);
        inputEl.value = transcript;
        send();
      },
      onError: (msg) => {
        setListening(false);
        addMessage("⚠ " + msg, "bot");
      },
      onStatus: (status) => setListening(status === "listening"),
    });
  }

  let listening = false;
  function setListening(on) {
    listening = on;
    listenBtn.classList.toggle("listen-pulse", on);
    const label = document.getElementById("listen-label");
    if (label) label.textContent = on ? "…" : SmartCropI18n.t("chat.speak");
  }

  function toggleTTS() {
    ttsOn = !ttsOn;
    speakBtn.classList.toggle("active", ttsOn);
    if (ttsOn) SmartCropVoice.speak("Text to speech is now on.", SmartCropI18n.lang);
    else SmartCropVoice.stopSpeaking();
  }

  document.addEventListener("DOMContentLoaded", () => {
    renderSuggestions();
    loadHistory();
    sendBtn.addEventListener("click", send);
    inputEl.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); send(); } });
    listenBtn.addEventListener("click", toggleListening);
    speakBtn.addEventListener("click", toggleTTS);
  });
})();
