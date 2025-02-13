import json, csv
from pathlib import Path
from typing import Any

from src.env_core.episode.state_space.piece import Piece


def load_config(path_config: Path) -> dict:
    try:
        with open(path_config, 'r') as config:
            return json.load(config)
    except FileNotFoundError:
        raise FileNotFoundError(f"'{path_config}' not found")
    except json.decoder.JSONDecodeError as e:
        raise ValueError(f"Cannot decode JSON '{path_config}'") from e


def read_map(path_map: Path) -> list[list[int]]:
    try:
        with open(path_map, 'r') as map_:
            return [[int(cell) for cell in row] for row in csv.reader(map_)]
    except FileNotFoundError:
        raise FileNotFoundError(f"'{path_map}' not found.")
    except ValueError as e:
        raise ValueError(f"Cannot decode CSV '{path_map}'")


def init_piece(piece_vals: dict[str, Any], coordinates: list[int]) -> Piece:
    try:
        return Piece(
            is_terminal=piece_vals["is_terminal"],
            location=coordinates,
            start_location=coordinates,
            reward=piece_vals["reward"],
            is_visitable=piece_vals["is_visitable"],
            character=piece_vals["character"],
            color=piece_vals["color"],
        )
    except KeyError as e:
        raise KeyError(f"Piece has no attribute: {e}") from e


def load_map(path_config: Path, path_map: Path) -> list[list[Piece]]:
    config = load_config(Path(path_config))
    map_ = read_map(Path(path_map))

    return [
        # TODO no default specified for config.get()
        [init_piece(config.get(str(piece_id)), [x, y]) for y, piece_id in enumerate(row)]
        for x, row in enumerate(map_)
    ]
