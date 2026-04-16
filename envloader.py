import os
from enum import Enum


class EnvItems(str, Enum):
    DEEPL_API_KEY = "DEEPL_API_KEY"
    CLAUDE_API_KEY = "CLAUDE_API_KEY"
    INPUT_FOLDER = "INPUT_FOLDER"
    OUTPUT_FOLDER = "OUTPUT_FOLDER"


def envloader(item: EnvItems) -> str:
    loaded_item = os.getenv(item.value)

    if not loaded_item:
        raise ValueError("Item not found in the .env file!")

    return loaded_item
