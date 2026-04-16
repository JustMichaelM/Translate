import deepl


class DeepLProvider:
    def __init__(self, api_key: str):
        self.translator = deepl.Translator(api_key)

    def translate_texts(self, texts: list[str], target_lang: str) -> list[str]:
        results = self.translator.translate_text(text=texts, target_lang=target_lang)
        if isinstance(results, list):
            return [r.text for r in results]
        return [results.text]
