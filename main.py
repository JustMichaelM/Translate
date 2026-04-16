from Translator import Translator
from envloader import envloader


def main():
    api_key: str = envloader()
    translator_agent = Translator(api_key=api_key)

    text = "Hello World"
    result = translator_agent.translate(text=text, target_lang="PL")

    print(f"Angielski: {text}")
    print(f"Tłumaczenie {result}")


if __name__ == "__main__":
    main()
