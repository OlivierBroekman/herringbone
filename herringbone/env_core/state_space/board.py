from pathlib import Path

from herringbone.env_core.utils.map_loader import load_map
from herringbone.env_core.utils.color import Color

class Board:
    def __init__(
            self,
            path_config: Path,
            path_map: Path
    ):
        self.pieces = load_map(path_config, path_map)

    #TODO: depricated? or?
    def observe_pieces(
            self
    ) -> dict:
        pass

    def __str__(
            self
    ):
        len_char = max(len(p.get_character() or '') for row in self.pieces for p in row)  # TODO print state values rather than chars
        num_cols = len(self.pieces[0]) if self.pieces else 0

        grid = f"╔{('═' * (len_char + 2) + '╦') * (num_cols - 1)}{'═' * (len_char + 1)}═╗\n"

        for i_row, row in enumerate(self.pieces):
            grid += f"║ {" ║ ".join(
                f"{Color.parse_color(p.get_color()).value}{((p.get_character() or '?').center(len_char))}{Color.RESET.value}"
                for p in row)} ║\n"

            if i_row < len(self.pieces) - 1:
                grid += "╠" + ('═' * (len_char + 2) + '╬') * (num_cols - 1) + '═' * (len_char + 1) + "═╣\n"

        grid += f"╚{('═' * (len_char + 2) + '╩') * (num_cols - 1) + '═' * (len_char + 1)}═╝"
        return grid
