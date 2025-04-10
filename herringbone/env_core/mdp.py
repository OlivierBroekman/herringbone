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
        gamma: float = 0.9,
    ):  
        self.seed = seed
        random.seed(self.seed)
        assert 0 <= gamma <= 1
        self.gamma = gamma
        self._board = Board(state_config, map)
        self._actions = load_actions(action_config)
        self._transition_matrices = transition_matrices or {
            action: TransitionMatrix(mdp=self, action=action)
            for action in self.get_actions()
        }
        if start_coords:
            self.start_state = self.get_board().states[start_coords[0]][start_coords[1]]
        else:
            self.start_state = None

    # Setters and getters
    def get_start_state(self) -> State:
        # check if a random state needs to be generated
        if self.start_state:
            return self.start_state
        non_terminal_states = [
            s for s in self.get_states() if not s.get_is_terminal()
        ]  # make sure the agent does not start in a terminal state
        return random.choice(non_terminal_states)

    def get_actions(self) -> list[Action]:
        return self._actions

    def get_board(self) -> Board:
        return self._board

    def get_states(self) -> list[State]:
        return [state for row in self._board.states for state in row]

    def get_next_state(self, state: State, action: Action) -> State:
        """Pick a successor state from states with the highest transition probability at random."""
        candidates = self.get_transition_matrices()[action].get_matrix()[state]
        return random.choice(
            [s for s in candidates if candidates[s] == max(candidates.values())]
        )

    def set_transition_matrices(self, new_matrices: dict[Action, TransitionMatrix]):
        self._transition_matrices = new_matrices

    def get_transition_matrices(self) -> dict[Action, TransitionMatrix]:
        return self._transition_matrices

    def get_gamma(self) -> float:
        return self.gamma
