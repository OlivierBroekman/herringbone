from pathlib import Path
from src.env_core.utils.map_loader import load_map


class Board:
    def __init__(self, path_config: Path, path_map: Path):
        self.pieces = load_map(path_config, path_map)

    def observe_pieces(self) -> dict:
        pass  # TODO ignore static pieces?

    def __str__(self):
        horizon = f"+{'----+' * len(self.pieces[0])}"

        return f"{horizon}\n{'\n'.join(
            f"| {' | '.join(f'{(p.character or "?"):>2}' for p in row)} |\n{horizon}"
            for row in self.pieces
        )}"
