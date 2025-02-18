
import os


from pathlib import Path
from src.env_core.utils.map_loader import load_map


class Board:
    def __init__(self, path_config: Path, path_map: Path):
        self.pieces = load_map(path_config, path_map)

    def observe_pieces(self) -> dict:
        pass  # TODO ignore static pieces?

    def __str__(self):  # TODO Color enum
        num_sep = len(self.pieces[0]) - 1
        grid = f"╔{'═══╦' * num_sep}═══╗\n"

        for i_row, row in enumerate(self.pieces):
            grid += "║ " + " ║ ".join(
                f"{p.color.encode('utf-8').decode('unicode_escape')}{(p.character or '?')}\033[0m" for p in
                row) + " ║\n"
            if i_row < len(self.pieces) - 1:
                grid += f"╠{'═══╬' * num_sep}═══╣\n"

        grid += f"╚{'═══╩' * num_sep}═══╝"
        return grid

board = Board(Path('src/env_core/config/piece_config.json'), Path('src/env_core/maps/example.csv'))
print(board)