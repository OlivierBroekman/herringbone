from action_space.action import Action
from state_space.board import Board
from state_space.piece import Piece

class Policy:
    def __init__(self, actions: list[Action], board: Board, policy: dict[Piece, dict[Action, float]] = None):
        self._actions = actions
        self._board = board
        if policy != None: self._policy = policy
        else: self._policy = self.create_default_policy(actions, board)

    def create_default_policy(self, actions: list[Action], board: Board) -> dict[Piece, dict[Action, float]]:
        """
        Creates a default, uniform policy,
        Where every action is just as likely as any other in any state.

        Arguments:
            actions: list[Action]: List of actions retrieved from action_config.json
            board: Board: Board retrieved from piece_config.json

        Returns:
            dict[Piece, dict[Action, float]]: A nested dictionary mapping states and actions to probabilities
        """
        
        states = [state for row in board for state in row]
        m_actions = len(actions)

        policy = {state: {action: (1/m_actions) for action in actions} for state in states}

        return policy
    
    # Setters and getters
    @property
    def actions(self) -> list[Action]:
        return self._actions
    
    @actions.setter
    def actions(self, new_actions: list[Action]):
        self._actions = new_actions
    
    @property
    def board(self) -> Board:
        return self._board
    
    @board.setter
    def board(self, new_board):
        self._board = new_board

    @property
    def policy(self) -> list[list[float]]:
        return self._policy
    
    @policy.setter
    def policy(self, new_policy: list[list[float]]):
        self._policy = new_policy