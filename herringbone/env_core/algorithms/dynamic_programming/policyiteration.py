import numpy as np

from herringbone.env_core.action_space import Action
from herringbone.env_core.state_space import Piece, Board
from herringbone.env_core.mdp import MDP
from herringbone.env_core.algorithms import Algorithm, Policy

class PolicyIteration(Algorithm):
    def __init__(
            self, 
            mdp: MDP, 
            theta_threshold: float, 
            gamma: float
            ):
        
        assert 0 <= theta_threshold <= 1 and 0 <= gamma <= 1
        self._mdp = mdp
        self._policy = Policy(mdp=self.get_mdp()).get_policy()
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
        self, new_policy: dict[Piece, dict[Action, float]]
        ):

        self._policy = new_policy
    
    def get_policy(
        self
        ) -> dict[Piece, dict[Action, float]]:

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
            ) -> tuple[Policy, dict[Piece, float]]:
        
        """
        Policy Iteration algorithm based on pseudocode by: 
        Reinforcement Learning: An Introduction by Sutton, R. & Barto, A.
        """

        def policy_evaluation(
                policy: Policy,
                mdp: MDP
                ) -> dict[Piece, float]:
            """
            Policy Evaluation algorithm, based on 
            Reinforcement Learning: An Introduction by Sutton, R. & Barto, A.
            """
            
            # We only need to initialise delt and state values
            delta = 0
            state_values = {state: 0 for state in states}

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
                    state_values[state] = new_value
                    
                    # Stopping criterion
                    delta = max(delta, abs(old_value - state.value))

                    return state_values
        
        def action_evaluation(
                state: Piece, 
                state_values: dict[Piece, float]
                ) -> dict[Action, float]:
            """Action evaluation"""

            actions = mdp.get_actions()

            # Set initial action values to zero
            action_values = {action: 0 for action in actions}

            # Add the value of each action to the dict
            for action in actions:
                for new_state, transition_probability in mdp.get_transition_matrices()[action][state].items():
                    action_values[action] += (transition_probability 
                                              * (state.get_reward() 
                                                 + self.get_gamma() 
                                                 * state_values[new_state]))
            return action_values
        
        states = self.get_mdp().get_states()
        policy = self.get_policy()
        mdp = self.get_mdp()

        # Policy Improvement
        while True:

            policy_stable = True
            state_values = policy_evaluation(policy=policy, mdp=mdp)

            for state in states:
                # Get current chosen action, based on the policy
                # keys = list(policy[state].keys())
                # chosen_action_idx = np.argmax(policy[state].values())
                # chosen_action = keys[chosen_action_idx]

                chosen_action = max(policy[state], key=policy[state].get)

                # Get the value of each action
                action_values = action_evaluation(state=state, state_values=state_values)

                # Use np.argmax to determine the best action, based on the values
                # keys = list(action_values.keys())
                # best_action_idx = np.argmax(action_values.values())
                # best_action = keys[best_action_idx]

                best_action = max(action_values, key=action_values.get)

                if chosen_action != best_action:
                    policy_stable = False
                
                # Update the policy
                policy[state] = {k: (1 if v == best_action else 0) for k, v in policy[state].items()}

                # If we have converged, stop the algorithm and return the policy with its evaluation
                if policy_stable:
                    return policy, state_values