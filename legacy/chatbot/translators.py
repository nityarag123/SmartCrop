def translate_text(text: str, from_language: str = 'auto', to_language: str = 'en') -> str:
    """
    Bypass translation and return the original text (English only mode).
    """
    return text

def translate_to_english(text: str) -> str:
    """
    Bypass translation and return the original text.
    """
    return translate_text(text, to_language='en')

def translate_from_english(text: str, target_lang: str) -> str:
    """
    Bypass translation and return the original text.
    """
    return translate_text(text, from_language='en', to_language=target_lang)
