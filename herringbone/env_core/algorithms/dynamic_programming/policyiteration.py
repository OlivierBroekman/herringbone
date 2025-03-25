import numpy as np

from herringbone.env_core.action_space import Action
from herringbone.env_core.state_space import State, Board
from herringbone.env_core.mdp import MDP
from herringbone.env_core.algorithms import Algorithm, Policy

class PolicyIteration(Algorithm):
    def __init__(
        self, 
        mdp: MDP, 
        theta_threshold: float, 
    ):
        
        assert 0 <= theta_threshold <= 1
        self._mdp = mdp
        self._policy = Policy(mdp=self.get_mdp())
        self._board = mdp.get_board()
        self._actions = mdp.get_actions()
        self._theta_threshold = theta_threshold

    
    # Setters and getters    
    def get_mdp(
            self
    ) -> MDP:

        return self._mdp

    def set_policy(
            self,
            new_policy: Policy
    ):

        self._policy = new_policy
    
    def get_policy(
            self
    ) -> Policy:

        return self._policy
    
    def get_board(
            self
    ) -> Board:

        return self._board
    
    def get_actions(
            self
    ) -> list[Action]:

        return self._actions
    
    def get_theta_threshold(
            self
    ) -> float:

        return self._theta_threshold
    
    def run(
            self
    ) -> tuple[Policy, dict[State, float]]:
        
        """
        Policy Iteration algorithm based on pseudocode by: 
        Reinforcement Learning: An Introduction by Sutton, R. & Barto, A.
        """

        def policy_evaluation(
                policy: dict[State, dict[Action, float]],
                mdp: MDP
        ) -> dict[State, float]:
            """
            Policy Evaluation algorithm, based on 
            Reinforcement Learning: An Introduction by Sutton, R. & Barto, A.
            """
            
            # We only need to initialise delt and state values
            delta = 1
            state_values = {state: 0 for state in states}

            while delta >= self.get_theta_threshold():
                delta = 0
                for state in states:
                    old_value = state_values[state]
                    new_value = 0
                    # Loop over all of the possible actions given by the policy
                    for action, action_probability in policy[state].items():
                        # Get all possible new states for each action, given by the transition matrix
                        for new_state, transition_probability in mdp.get_transition_matrices()[action].get_matrix()[state].items():
                            # Calculate the expected value of the state
                            new_value += (action_probability 
                                          * transition_probability 
                                          * (state.get_reward() 
                                             + gamma
                                             * state_values[new_state]))
                    
                    state_values[state] = new_value
                    
                    # Stopping criterion
                    delta = max(delta, abs(old_value - state_values[state]))

            return state_values
        
        def action_evaluation(
                state: State, 
                state_values: dict[State, float]
        ) -> dict[Action, float]:
            """Action evaluation"""

            actions = mdp.get_actions()

            # Set initial action values to zero
            action_values = {action: 0 for action in actions}

            # Add the value of each action to the dict
            for action in actions:
                for new_state, transition_probability in mdp.get_transition_matrices()[action].get_matrix()[state].items():
                    action_values[action] += (transition_probability 
                                              * (state.get_reward() 
                                                 + gamma 
                                                 * state_values[new_state]))
            return action_values
        
        states = self.get_mdp().get_states()
        policy = self.get_policy().get_policy()
        mdp = self.get_mdp()
        gamma = mdp.get_gamma()

        # Policy Improvement
        while True:

            policy_stable = True
            state_values = policy_evaluation(policy=policy, mdp=mdp)

            for state in states:
                # Get current chosen action, based on the policy
                chosen_action = max(policy[state], key=policy[state].get)

                # Get the value of each action
                action_values = action_evaluation(state=state, state_values=state_values)

                # Find the best action out of the action values
                best_action = max(action_values, key=action_values.get)

                # Update the policy
                policy[state] = {act: (1 if act == best_action else 0) for act in policy[state].keys()}

                if chosen_action != best_action:
                    policy_stable = False

            # If we have converged, stop the algorithm and return the policy with its evaluation
            if policy_stable:
                return Policy(mdp=mdp, policy=policy), state_values