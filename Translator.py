import deepl


class Translator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.translator = deepl.Translator(api_key)

    def translate(self, text: str, target_lang: str):
        result = self.translator.translate_text(text=text, target_lang=target_lang)

        if isinstance(result, list):
            translated = result[0].text
        else:
            translated = result.text

        return translated
