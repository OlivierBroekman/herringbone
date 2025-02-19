from algorithm import Algorithm
from policy import Policy
from state_space.board import Board
from state_space.piece import Piece
from action_space.action import Action

class PolicyIteration(Algorithm):
    def __init__(self, board: Board, actions: list[Action], theta_threshold: float, gamma: float):
        assert 0 <= theta_threshold <= 1 and 0 <= gamma <= 1
        self._policy = Policy()
        self._board = board
        self._actions = actions
        self._theta_threshold = theta_threshold
        self._gamma = gamma

    
    # Setters and getters
    # @property
    # def policy(self) -> Policy:
    #     return self._policy
    
    # @policy.getter
    # def policy(self, new_policy: Policy):
    #     self._policy = new_policy

    # Setters and getters
    @property
    def board(self) -> Board:
        return self._board
    
    @board.getter
    def board(self, new_board: Board):
        self.board = new_board

    @property
    def actions(self) -> list[Action]:
        return self._actions
    
    @actions.getter
    def actions(self, new_actions: list[Action]):
        self._actions = new_actions

    @property
    def theta_threshold(self) -> float:
        return self._theta_threshold
    
    @theta_threshold.getter
    def theta_threshold(self, new_theta):
        self._theta_threshold = new_theta

    @property
    def gamma(self) -> float:
        return self._gamma
    
    @gamma.getter
    def gamma(self, new_gamma: float):
        self._gamma = new_gamma

    
    def run(self) -> Policy:
        # Policy Evaluation

        delta = 0
        
        states = []
        while delta < self._theta_threshold:
            for state in states:
                old_value = state.value()

                new_value = 0

                delta = max(delta, abs(old_value - new_value))
            
            return 0
        
        # Policy Improvement
        policy_stable = True

        for state in states:
            old_action = self.policy
    