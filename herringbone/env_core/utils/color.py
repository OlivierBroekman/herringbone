from enum import Enum

class Color(Enum):
    RED = "\033[31m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    RESET = "\033[0m"

    @staticmethod
    def parse_color(
            color: str
    ):
        return Color.__members__.get(color.upper(), Color.RESET)