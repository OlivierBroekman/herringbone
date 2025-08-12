from csv import reader
from typing import Any
from pathlib import Path

from herringbone.env_core.utils.config_loader import load_config
from herringbone.env_core.state_space.state import State


def read_map(path_map: Path) -> list[list[int]]:
    try:
        with open(path_map, "r", encoding="utf-8") as map_:
            return [[int(cell) for cell in row] for row in reader(map_)]
    except FileNotFoundError:
        raise FileNotFoundError(f"'{path_map}' not found.")
    except ValueError:
        raise ValueError(f"Cannot decode CSV '{path_map}'")


def init_state(
    state_vals: dict[str, Any], coordinates: list[int, int], idx: int | None = None
) -> State:
    try:
        return State(
            is_terminal=state_vals["is_terminal"],
            location=coordinates,
            reward=state_vals["reward"],
            character=state_vals["character"],
            color=state_vals["color"],
            idx=idx,
        )
    except KeyError as e:
        raise KeyError(f"State has no attribute: {e}") from e


def load_map(
    path_config: Path | str,
    map_data: Path | str | list[list[int]]
) -> list[list[State]]:
    path_config = Path(path_config)

    if isinstance(map_data, (str, Path)):
        map_data = Path(map_data)
        map_ = read_map(map_data)
        map_source = map_data
    elif isinstance(map_data, list):
        map_ = map_data
        map_source = "<in-memory map>"
    else:
        raise TypeError(
            f"map_data must be Path, str (raw path), or list[list[int]], not {type(map_data).__name__}"
        )

    config = load_config(path_config)

    def get_state(state_id: int, coordinates: list[int, int], idx: int):
        try:
            return init_state(config[str(state_id)], coordinates, idx)
        except KeyError:
            raise KeyError(
                f"Unknown state ID '{state_id}' found at {coordinates} in {map_source}."
            )

    return [
        [
            get_state(state_id, [x, y], x * len(row) + y)
            for y, state_id in enumerate(row)
        ]
        for x, row in enumerate(map_)
    ]
