from enum import Enum


class NameHandling(Enum):
    """Options for handling character names in subtitles"""

    REMOVE = 1  # Remove names completely
    PREFIX = 2  # Move to start: "Name: line"
