/* ============================================================
   SmartCrop — voice utilities
   Speech-to-text (Web Speech API) and text-to-speech.
   Gracefully reports when the browser does not support them.
   ============================================================ */

const SmartCropVoice = (() => {
  const LANG_CODES = {
    en: "en-IN", hi: "hi-IN", te: "te-IN", ta: "ta-IN", gu: "gu-IN",
  };

  let recognition = null;
  let listening = false;

  function speechSupported() {
    return "SpeechRecognition" in window || "webkitSpeechRecognition" in window;
  }

  function startRecognition({ lang = "en", onResult, onError, onStatus }) {
    if (!speechSupported()) {
      if (onError) onError("Speech recognition is not supported in this browser. Please type your question instead.");
      return false;
    }
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SR();
    recognition.lang = LANG_CODES[lang] || "en-IN";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
      listening = true;
      if (onStatus) onStatus("listening");
    };
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript.trim();
      if (transcript && onResult) onResult(transcript);
    };
    recognition.onerror = (event) => {
      listening = false;
      const messages = {
        "not-allowed": "Microphone permission was denied. Please allow access and try again.",
        "no-speech": "No speech was detected. Please try again.",
        "network": "Speech recognition needs an internet connection.",
        "audio-capture": "No microphone found.",
      };
      if (onError) onError(messages[event.error] || "Speech recognition error. Please try again.");
      if (onStatus) onStatus("idle");
    };
    recognition.onend = () => {
      listening = false;
      if (onStatus) onStatus("idle");
    };

    try {
      recognition.start();
    } catch (_) {
      if (onError) onError("Could not start speech recognition. Please try again.");
    }
    return true;
  }

  function stopRecognition() {
    if (recognition) {
      try { recognition.stop(); } catch (_) { /* noop */ }
    }
    listening = false;
  }

  function ttsSupported() {
    return "speechSynthesis" in window;
  }

  function speak(text, lang = "en") {
    if (!ttsSupported()) return false;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = LANG_CODES[lang] || "en-IN";
    utterance.rate = 0.85;
    utterance.pitch = 1;
    const voices = window.speechSynthesis.getVoices();
    const match = voices.find((v) => v.lang && v.lang.toLowerCase().startsWith(LANG_CODES[lang].slice(0, 2)));
    if (match) utterance.voice = match;
    window.speechSynthesis.speak(utterance);
    return true;
  }

  function stopSpeaking() {
    if (ttsSupported()) window.speechSynthesis.cancel();
  }

  return { speechSupported, startRecognition, stopRecognition, ttsSupported, speak, stopSpeaking };
})();
