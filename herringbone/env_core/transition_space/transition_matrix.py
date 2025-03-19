from copy import deepcopy
import numpy as np

from herringbone.env_core.action_space.action import Action
from herringbone.env_core.state_space.board import Board
from herringbone.env_core.state_space.state import State
from herringbone.env_core.mdp import MDP

class TransitionMatrix:
    """This class represents a state transition matrix."""
    def __init__(
            self, 
            mdp: MDP, 
            action: Action
    ):
        
        self._mdp = mdp
        self._action = action
        self._matrix = self._build_transition_matrix(board=mdp.get_board(), action=action)
        
    
    def _build_transition_matrix(
            self,
            board: Board,
            action: Action
    ) -> dict[State, dict[State, float]]:
            """Build the transition matrix based on the given board and action."""
            states = [state for row in board.states for state in row]

            board_shape = (len(board.states), len(board.states[0]))

            directions = action.get_directions()
            probabilities = action.get_probabilities()
            outer = {state: {p: 0. for p in states} for state in states}


            # 2D ASSUMPTION 
            # Assign transition probabilities
            for state in states:
                idx = state.get_location()
                for direction, probability in zip(directions, probabilities):
                    # Make sure probabilities are only added for locations inside of bounds
                    new_idx = [np.clip(idx[0] + direction[0], a_min=0, a_max=board_shape[0] - 1),
                                np.clip(idx[1] + direction[1], a_min=0, a_max=board_shape[1] - 1)]
                    new_state = board.states[new_idx[0]][new_idx[1]]
                    outer[state][new_state] += probability
            return outer


    # Setters and getters    
    def get_mdp(
            self
    ):
        return self._mdp
    
    def get_action(
            self
    ) -> Action:
        return self._action
    
    def set_matrix(
            self, 
            new_matrix: dict[State, dict[State, float]]
    ):
        self._matrix = new_matrix
    
    def get_matrix(
            self
    ) -> dict[State, dict[State, float]]:
        return self._matrix

    def get_successor_state(
            self,
            state: State
    ) -> dict[State, float]:
        return {
            state_prime: prob_trans
            for state_prime, prob_trans in self.get_matrix()[state].items() if prob_trans != 0
            }

    def __str__(
            self
    ):
        pass