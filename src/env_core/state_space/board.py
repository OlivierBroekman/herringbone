import os
from enum import Enum
from pathlib import Path
from src.env_core.utils.map_loader import load_map


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


class Board:
    def __init__(
            self, 
            path_config: Path, 
            path_map: Path
            ):
        
        self.pieces = load_map(path_config, path_map)

    def observe_pieces(
            self
            ) -> dict:
        
        pass

    def __str__(
            self
            ):
        
        len_char = max(len(p.character or '') for row in self.pieces for p in row)
        num_cols = len(self.pieces[0]) if self.pieces else 0

        grid = f"╔{('═' * (len_char + 2) + '╦') * (num_cols - 1)}{'═' * (len_char + 1)}═╗\n"

        for i_row, row in enumerate(self.pieces):
            grid += f"║ {" ║ ".join(
                f"{Color.parse_color(p.color).value}{((p.character or '?').center(len_char))}{Color.RESET.value}"
                for p in row)} ║\n"

            if i_row < len(self.pieces) - 1:
                grid += "╠" + ('═' * (len_char + 2) + '╬') * (num_cols - 1) + '═' * (len_char + 1) + "═╣\n"

        grid += f"╚{('═' * (len_char + 2) + '╩') * (num_cols - 1) + '═' * (len_char + 1)}═╝"
        return grid

# board = Board(Path('src/env_core/config/piece_config.json'), Path('src/env_core/maps/example.csv'))
# print(board)
