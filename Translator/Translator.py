import pysrt
import re
import os
from pathlib import Path
from typing import Optional
from NameHandling import NameHandling
from Providers import TranslationProviderProtocol


class Translator:
    def __init__(
        self, provider: TranslationProviderProtocol, chunk: int, target_lang: str = "PL"
    ):
        self.provider = provider

    def translate(self): ...

    # def __srt_converter(self, path: str) -> pysrt.SubRipFile:
    #     """Loads a .srt file and returns a SubRipFile object"""

    #     if not path.endswith(".srt"):
    #         raise ValueError(f"The file must have the extension .srt, received: {path}")

    #     subs = pysrt.open(path, encoding="utf-8")
    #     return subs

    # def __extract_name_and_text(self, text: str) -> tuple[str, str]:
    #     """
    #     Extract character name and clean dialogue text

    #     Format: "dialogue text.  Character_Name"
    #     Returns: (name, clean_text)
    #     """
    #     # Regex: two+ spaces, then name at the end
    #     match = re.search(r"(.+?)\s{2,}([A-Za-z_]+)$", text)

    #     if match:
    #         clean_text = match.group(1).strip()
    #         name = match.group(2).strip()
    #         return name, clean_text

    #     # If no name found, return empty string and full text
    #     return "", text.strip()

    # def __apply_name_handling(
    #     self, name: str, translated_text: str, mode: NameHandling
    # ) -> str:
    #     """Apply selected name handling strategy"""
    #     if not name:
    #         return translated_text

    #     if mode == NameHandling.REMOVE:
    #         return translated_text

    #     elif mode == NameHandling.PREFIX:
    #         return f"{name}: {translated_text}"

    #     return translated_text

    # def __extract_texts(self, group: list) -> tuple[list[str], list[str]]:
    #     """
    #     Extract texts and names from subtitle group
    #     Returns: (list_of_names, list_of_clean_texts)
    #     """
    #     names = []
    #     texts = []

    #     for sub in group:
    #         name, clean_text = self.__extract_name_and_text(sub.text)
    #         names.append(name)
    #         texts.append(clean_text)

    #     return names, texts

    # def __apply_translations(
    #     self, group: list, translations, names: list[str], name_mode: NameHandling
    # ) -> None:
    #     """Apply translations to subtitle group with name handling"""
    #     for i, sub in enumerate(group):
    #         if isinstance(translations, list):
    #             translated = translations[i].text
    #         else:
    #             translated = translations.text

    #         # Apply selected name strategy
    #         sub.text = self.__apply_name_handling(names[i], translated, name_mode)

    # def translate_from_file(
    #     self,
    #     path: str,
    #     chunk: int,
    #     name_handling: NameHandling,
    #     target_lang: str = "PL",
    # ) -> str:
    #     """
    #     Translates an .srt file

    #     Args:
    #         path: Path to the .srt file
    #         chunk: How many strings to translate at once (for context)
    #         target_lang: Target language (e.g., 'PL', 'EN', 'JA')

    #     Returns:
    #         Path to the translated file
    #     """

    #     subs = self.__srt_converter(path=path)

    #     print(f"{len(subs)} subtitles loaded. Translating in groups of {chunk}...")

    #     for i in range(0, len(subs), chunk):
    #         group = subs[i : i + chunk]
    #         names, texts = self.__extract_texts(group)
    #         translations = self.translator.translate_text(
    #             text=texts, target_lang=target_lang
    #         )
    #         self.__apply_translations(group, translations, names, name_handling)

    #         print(f"Translated subtitles {i + 1}-{min(i + chunk, len(subs))}")

    #     # Zapisz
    #     output_file = path.replace(".srt", f"_{target_lang.lower()}.srt")
    #     subs.save(output_file, encoding="utf-8")
    #     print(f"✅ Saved: {output_file}")

    #     return output_file

    # def translate_from_folder(
    #     self,
    #     folder_path: str,
    #     chunk: int,
    #     target_lang: str,
    #     name_handling: NameHandling = NameHandling.PREFIX,
    #     output_folder: Optional[str] = None,
    # ) -> list[str]:
    #     """
    #     Translate all .srt files in a folder

    #     Args:
    #         folder_path: Path to folder containing .srt files
    #         chunk: How many subtitles to translate at once
    #         target_lang: Target language code (e.g. 'PL', 'EN', 'JA')
    #         name_handling: How to handle character names
    #         output_folder: Where to save translated files (default: same as input)

    #     Returns:
    #         List of paths to translated files
    #     """
    #     folder = Path(folder_path)

    #     if not folder.exists():
    #         raise FileNotFoundError(f"Folder not found: {folder_path}")

    #     if not folder.is_dir():
    #         raise ValueError(f"Path is not a folder: {folder_path}")

    #     # Find all .srt files
    #     srt_files = list(folder.glob("*.srt"))

    #     if not srt_files:
    #         print(f"⚠️  No .srt files found in: {folder_path}")
    #         return []

    #     print(f"Found {len(srt_files)} .srt file(s)")

    #     # Translate each file
    #     translated_files = []
    #     for srt_file in srt_files:
    #         try:
    #             print(f"\n{'=' * 50}")
    #             print(f"Processing: {srt_file.name}")
    #             print("=" * 50)

    #             output_path = self.translate_from_file(
    #                 path=str(srt_file),
    #                 chunk=chunk,
    #                 target_lang=target_lang,
    #                 name_handling=name_handling,
    #             )

    #             # Move to output folder if specified
    #             if output_folder:
    #                 os.makedirs(output_folder, exist_ok=True)
    #                 new_path = os.path.join(
    #                     output_folder, os.path.basename(output_path)
    #                 )
    #                 os.rename(output_path, new_path)
    #                 output_path = new_path

    #             translated_files.append(output_path)

    #         except Exception as e:
    #             print(f"❌ Failed to translate {srt_file.name}: {e}")
    #             continue

    #     print(f"\n{'=' * 50}")
    #     print(
    #         f"✅ Successfully translated {len(translated_files)}/{len(srt_files)} files"
    #     )
    #     print("=" * 50)

    #     return translated_files
