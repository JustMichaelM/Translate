from Translator import Translator
from envloader import envloader
from NameHandling import NameHandling
from SubtitlesExtractor import SubtitlesExtractor


def main():
    folder_path: str = "/Users/michal/Documents/filmy/Anime/Moonlit Fantasy S1"
    output_path: str = "/Users/michal/Documents/filmy/Anime/Moonlit Fantasy S1/Napisy"
    # api_key: str = envloader()
    # translator_agent = Translator(api_key=api_key)

    # result = translator_agent.translate(
    #     path="/Users/michal/Documents/dev/python/Translate/e1-failed-hero.srt",
    #     chunk=10,
    #     name_handling=NameHandling.REMOVE,
    # )

    # print(result)

    sub_extractor = SubtitlesExtractor()
    sub_extractor.extract_from_folder(
        folder_path=folder_path, output_folder=output_path
    )


if __name__ == "__main__":
    main()
