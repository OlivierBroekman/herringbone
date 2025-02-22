from mdp import MDP
from algorithm import Algorithm
from policy import Policy
from state_space.board import Board
from state_space.piece import Piece
from action_space.action import Action

class PolicyIteration(Algorithm):
    def __init__(
            self, 
            mdp: MDP, 
            theta_threshold: float, 
            gamma: float
            ):
        
        assert 0 <= theta_threshold <= 1 and 0 <= gamma <= 1
        self._mdp = mdp
        self._policy = Policy(mdp=self.get_mdp)
        self._board = mdp.get_board()
        self._actions = mdp.get_actions()
        self._theta_threshold = theta_threshold
        self._gamma = gamma

    
    # Setters and getters
    def set_mdp(
        self, new_mdp: MDP
        ):

        self._mdp = new_mdp
    
    def get_mdp(
        self
        ) -> MDP:

        return self._mdp

    def set_policy(
        self, new_policy: Policy
        ):

        self._policy = new_policy
    
    def get_policy(
        self
        ) -> Policy:

        return self._policy

    def set_board(
        self, new_board: Board
        ):

        self._board = new_board
    
    def get_board(
        self
        ) -> Board:

        return self._board

    def set_actions(
        self, new_actions: list[Action]
        ):

        self._actions = new_actions
    
    def get_actions(
        self
        ) -> list[Action]:

        return self._actions

    def set_theta_threshold(
        self, new_theta_threshold: float
        ):

        self._theta_threshold = new_theta_threshold
    
    def get_theta_threshold(
        self
        ) -> float:

        return self._theta_threshold

    def set_gamma(
        self, new_gamma: float
        ):

        self._gamma = new_gamma
    
    def get_gamma(
        self
        ) -> float:

        return self._gamma


    
    def run(
            self
            ) -> Policy:
        
        # Policy Evaluation
        board = self.board

        states = [state for row in board for state in row]

        def expected_utility(state: Piece, action: Action, policy: Policy):            
            return 

        def policy_evaluation():
            delta = 0

            while delta <= self.theta_threshold:
                for state in states:
                    old_value = state.value
                    state.value = state.reward + self.gamma * sum()
                    delta = max(delta, abs(old_value - state.value))
            return
        
        # Policy Improvement
        policy_stable = True

        for state in states:
            old_action = self.policy
    