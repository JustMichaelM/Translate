import deepl
import pysrt
import re
from NameHandling import NameHandling


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

    def __extract_name_and_text(self, text: str) -> tuple[str, str]:
        """
        Extract character name and clean dialogue text

        Format: "dialogue text.  Character_Name"
        Returns: (name, clean_text)
        """
        # Regex: two+ spaces, then name at the end
        match = re.search(r"(.+?)\s{2,}([A-Za-z_]+)$", text)

        if match:
            clean_text = match.group(1).strip()
            name = match.group(2).strip()
            return name, clean_text

        # If no name found, return empty string and full text
        return "", text.strip()

    def __apply_name_handling(
        self, name: str, translated_text: str, mode: NameHandling
    ) -> str:
        """Apply selected name handling strategy"""
        if not name:
            return translated_text

        if mode == NameHandling.REMOVE:
            return translated_text

        elif mode == NameHandling.PREFIX:
            return f"{name}: {translated_text}"

        return translated_text

    def __extract_texts(self, group: list) -> tuple[list[str], list[str]]:
        """
        Extract texts and names from subtitle group
        Returns: (list_of_names, list_of_clean_texts)
        """
        names = []
        texts = []

        for sub in group:
            name, clean_text = self.__extract_name_and_text(sub.text)
            names.append(name)
            texts.append(clean_text)

        return names, texts

    def __apply_translations(
        self, group: list, translations, names: list[str], name_mode: NameHandling
    ) -> None:
        """Apply translations to subtitle group with name handling"""
        for i, sub in enumerate(group):
            if isinstance(translations, list):
                translated = translations[i].text
            else:
                translated = translations.text

            # Apply selected name strategy
            sub.text = self.__apply_name_handling(names[i], translated, name_mode)

    def translate(
        self,
        path: str,
        chunk: int,
        name_handling: NameHandling,
        target_lang: str = "PL",
    ) -> str:
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
            names, texts = self.__extract_texts(group)
            translations = self.translator.translate_text(
                text=texts, target_lang=target_lang
            )
            self.__apply_translations(group, translations, names, name_handling)

            print(f"Translated subtitles {i + 1}-{min(i + chunk, len(subs))}")

        # Zapisz
        output_file = path.replace(".srt", f"_{target_lang.lower()}.srt")
        subs.save(output_file, encoding="utf-8")
        print(f"✅ Saved: {output_file}")

        return output_file
