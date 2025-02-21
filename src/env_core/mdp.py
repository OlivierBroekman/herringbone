from action_space.action import Action
from env_core.action_space import action
from env_core.state_space.piece import Piece
from state_space.board import Board
from transition_space.transition_matrix import TransitionMatrix

class MDP:
    def __init__(
            self, 
            actions: list[Action],
            board: Board,
            transition_matrices: dict[Action, TransitionMatrix]
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
    def set_actions(
            self, 
            new_actions: list[Action]
            ):
        
        self._actions = new_actions
    
    def get_actions(
            self
            ) -> list[Action]:
        
        return self._actions
    
    def set_board(
            self, 
            new_board: Board
            ):
        
        self._board = new_board

    def get_board(
            self
            ) -> Board:
        
        return self._board
    
    def set_transition_matrices(self, 
                                new_matrices: dict[Action, TransitionMatrix]
                                ):
        
        self.transition_matrices = new_matrices

    def get_transition_matrices(
            self
            ) -> dict[Action, TransitionMatrix]:
        
        return self._transition_matrices

