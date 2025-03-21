from csv import reader
from typing import Any
from pathlib import Path

from herringbone.env_core.utils.config_loader import load_config
from herringbone.env_core.state_space.state import State


def read_map(path_map: Path) -> list[list[int]]:
    try:
        with open(path_map, 'r', encoding='utf-8') as map_:
            return [[int(cell) for cell in row] for row in reader(map_)]
    except FileNotFoundError:
        raise FileNotFoundError(f"'{path_map}' not found.")
    except ValueError:
        raise ValueError(f"Cannot decode CSV '{path_map}'")


def init_state(state_vals: dict[str, Any], coordinates: list[int, int]) -> State:
    try:
        return State(
            is_terminal=state_vals["is_terminal"],
            location=coordinates,
            reward=state_vals["reward"],
            is_visitable=state_vals["is_visitable"],
            character=state_vals["character"],
            color=state_vals["color"],
        )
    except KeyError as e:
        raise KeyError(f"State has no attribute: {e}") from e


def load_map(path_config: Path, path_map: Path) -> list[list[State]]:
    config = load_config(Path(path_config))
    map_ = read_map(Path(path_map))

    def get_state(state_id: int, coordinates: list[int, int]):
        try:
            return init_state(config[str(state_id)], coordinates)
        except KeyError:
            raise KeyError(
                f"Unknown state ID '{state_id}' found at {coordinates} in {path_map}."
            )

    return [
        [get_state(state_id, [x, y]) for y, state_id in enumerate(row)]
        for x, row in enumerate(map_)
    ]
