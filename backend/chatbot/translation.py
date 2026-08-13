"""Best-effort translation for the chatbot.

Uses ``deep-translator`` if installed (optional dependency). Without it,
responses stay in English and the caller is told so — SmartCrop never claims
to translate when it cannot.
"""
_LANG_MAP = {
    "en": "english",
    "hi": "hindi",
    "te": "telugu",
    "ta": "tamil",
    "gu": "gujarati",
}

_translator = None
_attempted = False


def _get_translator():
    global _translator, _attempted
    if _attempted:
        return _translator
    _attempted = True
    try:
        from deep_translator import GoogleTranslator
        _translator = GoogleTranslator
    except ImportError:
        _translator = None
    return _translator


def translate(text, to_lang):
    if to_lang in ("en", None, "") or not text:
        return text
    provider = _get_translator()
    if provider is None:
        return text
    try:
        return provider(source="auto", target=_LANG_MAP.get(to_lang, "en")).translate(text)
    except Exception:
        return text


def available():
    return _get_translator() is not None
