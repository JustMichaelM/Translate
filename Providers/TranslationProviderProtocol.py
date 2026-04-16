from typing import Protocol


class TranslationProviderProtocol(Protocol):
    """Protocol for translation providers"""

    def translate_texts(self, texts: list[str], target_lang: str) -> list[str]:
        """Translate list of texts to target language"""
        ...
