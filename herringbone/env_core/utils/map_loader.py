import csv, json
from typing import Any
from pathlib import Path

from herringbone.env_core.state_space.state import State


def load_config(
        path_config: Path
) -> dict:
    try:
        with open(path_config, 'r') as config:
            return json.load(config)
    except FileNotFoundError:
        raise FileNotFoundError(f"'{path_config}' not found")
    except json.decoder.JSONDecodeError as e:
        raise ValueError(f"Cannot decode JSON '{path_config}'") from e


def read_map(
        path_map: Path
) -> list[list[int]]:
    try:
        with open(path_map, 'r') as map_:
            return [[int(cell) for cell in row] for row in csv.reader(map_)]
    except FileNotFoundError:
        raise FileNotFoundError(f"'{path_map}' not found.")
    except ValueError:
        raise ValueError(f"Cannot decode CSV '{path_map}'")


def init_state(
        state_vals: dict[str, Any],
        coordinates: list[int]
) -> State:
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


def load_map(
        path_config: Path,
        path_map: Path
) -> list[list[State]]:
    config = load_config(Path(path_config))
    map_ = read_map(Path(path_map))

    return [
        # TODO no default specified for config.get()
        [init_state(config.get(str(state_id)), [x, y]) for y, state_id in enumerate(row)]
        for x, row in enumerate(map_)
    ]
