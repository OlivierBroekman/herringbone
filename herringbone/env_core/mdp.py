
from herringbone.env_core.action_space import Action
from herringbone.env_core.state_space import Piece, Board
from herringbone.env_core.transition_space import TransitionMatrix

class MDP:
    def __init__(
            self, 
            actions: list[Action],
            board: Board,
            transition_matrices: dict[Action, TransitionMatrix] = None
    ):
        self._actions = actions
        self._board = board
        if transition_matrices != None: self._transition_matrices = transition_matrices
        else: self._transition_matrices = {
            action: 
            TransitionMatrix(mdp=self, action=action)
            for action in self.get_actions()
            }
    
    # Setters and getters
    def get_actions(
            self
    ) -> list[Action]:
        return self._actions

    def get_board(
            self
    ) -> Board:
        return self._board
    
    def get_states(
            self
    ) -> list[Piece]:
        return [piece for row in self._board.pieces for piece in row]
    
    def set_transition_matrices(
            self, 
            new_matrices: dict[Action, TransitionMatrix]
    ):
        self._transition_matrices = new_matrices

    def get_transition_matrices(
            self
    ) -> dict[Action, TransitionMatrix]:
        return self._transition_matrices

