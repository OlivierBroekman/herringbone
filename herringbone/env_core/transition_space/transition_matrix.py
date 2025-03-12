from copy import deepcopy
import numpy as np

from env_core.action_space.action import Action
from env_core.state_space.board import Board
from env_core.state_space.piece import Piece
from env_core.mdp import MDP

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
                board: Board,
                action: Action
                ) -> dict[Piece, dict[Piece, float]]:
            """Build the transition matrix based on the given board and action."""
            states = [piece for row in board.pieces for piece in row]

            board_shape = (len(board.pieces), len(board.pieces[0]))

            directions = action.get_directions()
            probabilities = action.get_probabilities()

            inner = {piece: 0. for piece in states}
            outer = {piece: deepcopy(inner) for piece in states}

            # 2D ASSUMPTION 
            # Assign transition probabilities
            for piece in states:
                idx = piece.get_location()
                for direction, probability in zip(directions, probabilities):
                    # Make sure probabilities are only added for locations inside of bounds
                    new_idx = [np.clip(idx[0] + direction[0], a_min=0, a_max=board_shape[0] - 1),
                                np.clip(idx[1] + direction[1], a_min=0, a_max=board_shape[1] - 1)]
                    new_piece = board.pieces[new_idx[0]][new_idx[1]]
                    outer[piece][new_piece] += probability
            return outer


    # Setters and getters
    def set_mdp(
        self, 
        new_mdp: MDP):

        self._mdp = new_mdp
    
    def get_mdp(
        self
        ) -> MDP:

        return self._mdp
    
    def set_action(
        self, 
        new_action: Action):

        self._action = new_action
    
    def get_action(
        self
        ) -> Action:

        return self._action
    
    def set_matrix(
        self, 
        new_matrix: dict[Piece, dict[Piece, float]]):

        self._matrix = new_matrix
    
    def get_matrix(
        self
        ) -> dict[Piece, dict[Piece, float]]:

        return self._matrix

    def get_successor_state(
        self,
        state: Piece
    ) -> dict[Piece, float]:
        return {
            state_prime: prob_trans
            for state_prime, prob_trans in self.get_matrix()[state].items() if prob_trans != 0
            }

    def __str__(
        self
        ):

        pass