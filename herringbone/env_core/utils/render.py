from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from herringbone.env_core.state_space.board import Board
    from herringbone.env_core.state_space.state import State
    from herringbone.env_core.action_space.action import Action
    from herringbone.env_core.episode.episode import Trajectory
    from herringbone.env_core.mdp import MDP

from herringbone.env_core.utils.color import Color

import time

# Issues with circular imports??? i HATE this 
# TODO read this: https://www.reddit.com/r/learnpython/comments/zzgkxj/how_to_avoid_circular_imports_when_using_static/
# and this https://adamj.eu/tech/2021/05/13/python-type-hints-how-to-fix-circular-imports/


class Render:
    valid_render_modes = ["sar", "rewards", "ascii"]

    @staticmethod
    def preview_frame(board: Board, agent_state: State, render_mode: str, action: Action = None, t: int = 0) -> None:
        """Renders a single frame, which is a board with agent"""
        if render_mode.lower() not in Render.valid_render_modes:
            error_msg = f"Render error: {render_mode} is not a valid mode, please choose from: {', '.join(Render.valid_render_modes)}."
            raise RuntimeError(error_msg)

        if render_mode == "sar":
            print(f"t: {t} | S: {agent_state}, R: {agent_state.get_reward()}, A: {action}" ) 

        if render_mode == "rewards":
            print(Render.fancy_board(board, agent_state, lambda s: s.get_reward(), t))


        if render_mode == "ascii":
            print(Render.fancy_board(board, agent_state, lambda s: s.get_character(), t))

    @staticmethod
    def fancy_board(board: Board, agent_state: State, property_func=lambda s: s.get_character(), t: int = 0) -> str:
        """Builds an ascii board based on a property"""

        # Add agent as rendered state
        rendering_states = [[board.agent if s == agent_state else s for s in row] for row in board.states] if agent_state else board.states
        
        len_char = max(max(len(str(property_func(s)) or '') for row in board.states for s in row), len(board.agent.get_character()))
        num_cols = len(rendering_states[0]) if rendering_states else 0

        grid = f"╔{('═' * (len_char + 2) + '╦') * (num_cols - 1)}{'═' * (len_char + 1)}═╗\n"

        for i_row, row in enumerate(rendering_states):
            grid += f"║ {" ║ ".join(
                f"{Color.parse_color(s.get_color()).value}{(s.get_character() if s == board.agent else str(property_func(s)) or '?').center(len_char)}{Color.RESET.value}"
                for s in row)} ║\n"

            if i_row < len(rendering_states) - 1:
                grid += "╠" + ('═' * (len_char + 2) + '╬') * (num_cols - 1) + '═' * (len_char + 1) + "═╣\n"

        grid += f"╚{('═' * (len_char + 2) + '╩') * (num_cols - 1) + '═' * (len_char + 1)}═╝"
        return grid + f"[{t}]"
    
    @staticmethod
    def animate(mdp: MDP, trajectory: Trajectory, render_mode:str, pause: int = 0)-> None:
        #TODO: do we want to add clear to this?
        """Animates a trajectory"""
        board = mdp.get_board()
        T = len(trajectory.states)
        for t in range(T):
            action = None if t == T - 1 else trajectory.actions[t]
            Render.preview_frame(board, trajectory.states[t], render_mode, action, t)
            time.sleep(pause)
            
    
    @staticmethod 
    def preview_V(mdp: MDP, learned_V):
        """Renders a Value Function"""

        states_2d = mdp.get_board().states
        x, num_cols = len(states_2d), len(states_2d[0])
        V_values = [ [f'{v:.2f}' for v in learned_V.values()][i * num_cols:(i + 1) * num_cols] for i in range(x)]
    
        len_char = len(max([str(v) for row in V_values for v in row], key=len))
        
        grid = f"╔{('═' * (len_char + 2) + '╦') * (num_cols - 1)}{'═' * (len_char + 1)}═╗\n"

        for i_row, row in enumerate(V_values):
            grid += f"║ {" ║ ".join(
                f"{(v).center(len_char)}" for v in row
            )} ║\n"

            if i_row < len(V_values) - 1:
                grid += "╠" + ('═' * (len_char + 2) + '╬') * (num_cols - 1) + '═' * (len_char + 1) + "═╣\n"

        grid += f"╚{('═' * (len_char + 2) + '╩') * (num_cols - 1) + '═' * (len_char + 1)}═╝"
        print(grid)

    @staticmethod
    def preview_Q(mdp: MDP, learned_Q: dict[State, dict[Action, float]]) -> None:
        states_2d = mdp.get_board().states
        actions = mdp.get_actions()
        cell_width = len(f"{max(actions, key=lambda a: len(a.get_character()))}: {0:.2f}") + 2
        num_cols = len(states_2d[1])
        
        grid = f"╔{('═' * (cell_width + 2) + '╦') * (num_cols - 1)}{'═' * (cell_width + 1)}═╗\n"

        for i_row, row in enumerate(states_2d):
            for a in actions:
                grid += f"║ {"".join(
                    f"{" ║ ".join([f"{a.get_character()}: {learned_Q[state][a]:.2f}"]).center(cell_width)} ║ "
                    for state in row)}"
                grid += '' if a.get_id() == actions[-1].get_id() else '\n'
            grid += '\n'

            if i_row < len(states_2d) - 1:
                grid += "╠" + ('═' * (cell_width + 2) + '╬') * (num_cols - 1) + '═' * (cell_width + 1) + "═╣\n"

        grid += f"╚{('═' * (cell_width + 2) + '╩') * (num_cols - 1) + '═' * (cell_width + 1)}═╝"
        
        print(grid)
