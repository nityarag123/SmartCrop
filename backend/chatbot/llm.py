"""Optional LLM integration for the farm assistant.

Only used when LLM_API_KEY / OPENAI_API_KEY is configured and the ``openai``
package is installed. Never exposes the key to the browser.
"""
import os


class LLMService:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        self._client = None
        if self.api_key:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key)
            except ImportError:
                self._client = None

    def available(self):
        return self._client is not None

    def chat(self, message, system, lang="en"):
        if not self.available():
            raise RuntimeError("LLM not configured")
        lang_note = (
            f"Reply in {lang} (the farmer's language). " if lang != "en" else ""
        )
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": lang_note + message},
            ],
            temperature=0.5,
            max_tokens=400,
        )
        return response.choices[0].message.content.strip()


_llm = LLMService()


def get_llm():
    return _llm
