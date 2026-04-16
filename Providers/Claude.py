import anthropic


class ClaudeProvider:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def translate_texts(self, texts: list[str], target_lang: str) -> list[str]:
        translations = []
        return translations
