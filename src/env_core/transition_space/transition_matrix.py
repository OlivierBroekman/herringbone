from copy import deepcopy

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
        self._matrix = helper(board=mdp.get_board(), action=action)
        
        def helper(
                board: Board,
                action: Action
                ) -> dict[Piece, dict[Piece, float]]:
            
            states = [piece for row in board for piece in row]
            direction = action.get_direction() # !
            inner = {piece: 0. for piece in states}
            outer = {piece: deepcopy(inner) for piece in states}
            return outer


    # Setter and getter
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


    def __str__(
        self
        ):

        pass