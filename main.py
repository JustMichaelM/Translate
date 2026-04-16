from Translator import Translator
from envloader import envloader
from NameHandling import NameHandling
from SubtitlesExtractor import SubtitlesExtractor


def main():
    # folder_path: str = ""
    # output_path: str = ""

    # sub_extractor = SubtitlesExtractor()
    # sub_extractor.extract_from_folder(
    #     folder_path=folder_path, output_folder=output_path
    # )

    api_key: str = envloader()
    translator_agent = Translator(api_key=api_key)

    translator_agent.translate_folder(
        folder_path="/Users/michal/Documents/filmy/Anime/Moonlit Fantasy S2/Napisy",
        chunk=10,
        target_lang="PL",
        name_handling=NameHandling.REMOVE,
    )


if __name__ == "__main__":
    main()
