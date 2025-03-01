from herringbone import MDP, Algorithm, Policy, Board, Piece, Action

class PolicyIteration(Algorithm):
    def __init__(
            self, 
            mdp: MDP, 
            theta_threshold: float, 
            gamma: float
            ):
        
        assert 0 <= theta_threshold <= 1 and 0 <= gamma <= 1
        self._mdp = mdp
        self._policy = Policy(mdp=self.get_mdp).get_policy()
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
        board = self._board

        states = self._mdp.get_states()

        # state_values = {state: 0 for state in states}

        def expected_utility(
                state: Piece,
                action: Action, 
                mdp: MDP
                ) -> float: 
            
            """Get the expected utility of some state action pair"""
            
            # Get correct transition matrix for the given state/action pair. 
            # This matrix has a probability assigned of moving to that state given the initial state and action
            matrix = mdp.get_transition_matrices()[action][state]
            
            # Get the expected utility of the state by summing the product 
            # of all probabilities with the value of each successor state
            exp_utility = sum(probability * new_state.get_value()
                              for new_state, probability in matrix.items())
            return exp_utility

        def policy_evaluation(
                policy: Policy,
                mdp: MDP
                ):
            """
            Policy Evaluation algorithm, based on 
            Reinforcement Learning: An Introduction by Sutton, R. & Barto, A.
            """
            
            # We only need to initialise delta, as all states have already been given a default value of 0
            delta = 0

            while delta <= self.get_theta_threshold():
                for state in states:
                    old_value = state.get_value()
                    new_value = 0
                    # Loop over all of the possible actions given by the policy
                    for action, action_probability in policy[state].items():
                        # Get all possible new states for each action, given by the transition matrix
                        for new_state, transition_probability in mdp.get_transition_matrices()[action][state].items():
                            # Calculate the expected value of the state
                            new_value += (action_probability 
                                          * transition_probability 
                                          * (state.get_reward() 
                                             + self.get_gamma() 
                                             * new_state.get_value()))
                    
                    state.set_value(new_value)
                    
                    # Stopping criterion
                    delta = max(delta, abs(old_value - state.value))

                    # We do not need to return anything as the values are a field of the Piece class
        
        # Policy Improvement
        policy_stable = True

        for state in states:
            old_action = self.policy
    