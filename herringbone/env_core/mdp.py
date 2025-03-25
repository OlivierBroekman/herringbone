from pathlib import Path
import random

from herringbone.env_core.action_space import Action
from herringbone.env_core.state_space import State, Board
from herringbone.env_core.transition_space import TransitionMatrix
from herringbone.env_core.utils.actions_loader import load_actions


class MDP:
    def __init__(
        self,
        state_config: Path,
        map: Path,
        action_config: Path,
        transition_matrices: dict[Action, TransitionMatrix] | None = None,
        start_coords: tuple[int, int] | None = None,
        seed: int = 42,
        gamma: float = 0.9
    ):
        assert 0 <= gamma <= 1
        self._board = Board(state_config, map)
        self._actions = load_actions(action_config)
        self._transition_matrices = transition_matrices or {
            action: TransitionMatrix(mdp=self, action=action)
            for action in self.get_actions()
        }
        if start_coords:
            self.start_state = self.get_board().states[start_coords[0]][start_coords[1]]
        else:
            self.start_state = self.get_board().states[
                random.randint(0, len(self.get_board().states) - 1)
            ][random.randint(0, len(self.get_board().states[0]) - 1)]  # Arbitrary S_0
        random.seed(seed)

    # Setters and getters
    def get_actions(self) -> list[Action]:
        return self._actions

    def get_board(self) -> Board:
        return self._board

    def get_states(self) -> list[State]:
        return [state for row in self._board.states for state in row]

    def set_transition_matrices(self, new_matrices: dict[Action, TransitionMatrix]):
        self._transition_matrices = new_matrices

    def get_transition_matrices(self) -> dict[Action, TransitionMatrix]:
        return self._transition_matrices
    
    def get_gamma(self) -> float:
        return self.gamma
