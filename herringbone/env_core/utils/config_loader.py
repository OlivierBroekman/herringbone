import json
from pathlib import Path


def load_config(
    path_config: Path
) -> dict:
    try:
        with open(path_config, 'r', encoding='utf-8') as config:
            return json.load(config)
    except FileNotFoundError:
        raise FileNotFoundError(f"'{path_config}' not found")
    except json.decoder.JSONDecodeError as e:
        raise ValueError(f"Cannot decode JSON '{path_config}'") from e
