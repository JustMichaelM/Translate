import deepl
import pysrt


class Translator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.translator = deepl.Translator(api_key)

    def __srt_converter(self, path: str) -> pysrt.SubRipFile:
        """Loads a .srt file and returns a SubRipFile object"""

        if not path.endswith(".srt"):
            raise ValueError(f"The file must have the extension .srt, received: {path}")

        subs = pysrt.open(path, encoding="utf-8")
        return subs

    def __extract_texts(self, group: list) -> list[str]:
        """Extracts texts from a group of strings"""
        return [sub.text for sub in group]

    def __apply_translations(self, group: list, translations) -> None:
        """Applies translations to a group of subtitles"""
        for i, sub in enumerate(group):
            if isinstance(translations, list):
                sub.text = translations[i].text
            else:
                sub.text = translations.text

    def translate(self, path: str, chunk: int, target_lang: str) -> str:
        """
        Translates an .srt file

        Args:
            path: Path to the .srt file
            chunk: How many strings to translate at once (for context)
            target_lang: Target language (e.g., 'PL', 'EN', 'JA')

        Returns:
            Path to the translated file
        """

        subs = self.__srt_converter(path=path)

        print(f"{len(subs)} subtitles loaded. Translating in groups of {chunk}...")

        for i in range(0, len(subs), chunk):
            group = subs[i : i + chunk]
            texts = self.__extract_texts(group)

            translations = self.translator.translate_text(
                text=texts, target_lang=target_lang
            )

            self.__apply_translations(group, translations)

            print(f"Translated subtitles {i + 1}-{min(i + chunk, len(subs))}")

        # Zapisz
        output_file = path.replace(".srt", f"_{target_lang.lower()}.srt")
        subs.save(output_file, encoding="utf-8")
        print(f"✅ Saved: {output_file}")

        return output_file
