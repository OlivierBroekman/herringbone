from pathlib import Path

from herringbone.env_core.utils.config_loader import load_config
from herringbone.env_core.action_space.action import Action


def load_actions(
    path_config: Path
) -> list[Action]:
    config = load_config(path_config)
    return [Action(action) for action in config.values()]
