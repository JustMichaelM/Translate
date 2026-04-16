import os
from dotenv import load_dotenv


def envloader() -> str:
    load_dotenv()
    api_key = os.getenv("DEEPL_API_KEY")

    if not api_key:
        raise ValueError("DEEPL_API_KEY nie został znaleziony w pliku .env!")

    return api_key
