from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from herringbone.env_core.state_space.board import Board
    from herringbone.env_core.state_space.state import State
    from herringbone.env_core.action_space.action import Action
    from herringbone.env_core.episode.episode import Trajectory

from herringbone.env_core.utils.color import Color

# Issues with circular imports??? i HATE this 
# TODO read this: https://www.reddit.com/r/learnpython/comments/zzgkxj/how_to_avoid_circular_imports_when_using_static/
# and this https://adamj.eu/tech/2021/05/13/python-type-hints-how-to-fix-circular-imports/


class Render:
    valid_render_modes = ["sar", "rewards", "ascii"]

    @staticmethod
    def preview_frame(board: Board, agent_state: State, render_mode: str, action: Action = None, t: int = 0) -> None:
        if render_mode.lower() not in Render.valid_render_modes:
            error_msg = f"Render error: {render_mode} is not a valid mode, please choose from: {', '.join(Render.valid_render_modes)}."
            raise RuntimeError(error_msg)

        if render_mode == "sar":
            print(f"t: {t} | S: {agent_state}, R: {agent_state.get_reward()}, A: {action}" ) 

        if render_mode == "rewards":
            print(Render.fancy_board(board, agent_state, lambda s: s.get_reward(), t))


        if render_mode == "ascii":
            print(Render.fancy_board(board, agent_state, lambda s: s.get_character()))

    @staticmethod
    def fancy_board(board: Board, agent_state: State, property_func=lambda s: s.get_character(), t: int = 0) -> str:
        
        if agent_state:
            rendering_states = [[board.agent if s == agent_state else s for s in row] for row in board.states]
        else:
            rendering_states = board.states
        
        len_char = max(len(str(property_func(s)) or '') for row in rendering_states for s in row)
        num_cols = len(rendering_states[0]) if rendering_states else 0

        grid = f"╔{('═' * (len_char + 2) + '╦') * (num_cols - 1)}{'═' * (len_char + 1)}═╗\n"

        for i_row, row in enumerate(rendering_states):
            grid += f"║ {" ║ ".join(
                f"{Color.parse_color(s.get_color()).value}{(str(property_func(s)) or '?').center(len_char)}{Color.RESET.value}"
                for s in row)} ║\n"

            if i_row < len(rendering_states) - 1:
                grid += "╠" + ('═' * (len_char + 2) + '╬') * (num_cols - 1) + '═' * (len_char + 1) + "═╣\n"

        grid += f"╚{('═' * (len_char + 2) + '╩') * (num_cols - 1) + '═' * (len_char + 1)}═╝"
        return grid + f"[{t}]"