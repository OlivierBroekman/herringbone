import json
from pathlib import Path


def load_config(
    path_config: Path
) -> dict:
    try:
        with open(path_config, 'r', encoding='utf-8') as config:
            config_ = json.load(config)
            assert len(config_.keys()) >= 2
            return config_
    except FileNotFoundError:
        raise FileNotFoundError(f"'{path_config}' not found")
    except AssertionError:
        raise AssertionError(f"Found {len(config_.keys())} type(s) of state(s), 2 required.")
    except json.decoder.JSONDecodeError as e:
        raise ValueError(f"Cannot decode JSON '{path_config}'") from e
