from Translator import Translator
from envloader import envloader


def main():
    api_key: str = envloader()
    translator_agent = Translator(api_key=api_key)

    result = translator_agent.translate(
        path="/Users/michal/Documents/dev/python/Translate/e1-failed-hero.srt",
        chunk=10,
        target_lang="PL",
    )

    print(result)


if __name__ == "__main__":
    main()
