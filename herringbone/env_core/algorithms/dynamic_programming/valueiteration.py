from herringbone.env_core.action_space import Action
from herringbone.env_core.state_space import State, Board
from herringbone.env_core.mdp import MDP
from herringbone.env_core.algorithms import Algorithm, Policy


class ValueIteration(Algorithm):
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
            self, new_policy: Policy
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
    ) -> tuple[Policy, dict[State, float], dict[State, dict[Action, float]]]:
        """Value Iteration algorithm based on pseudocode by: 
        Reinforcement Learning: An Introduction by Sutton, R. & Barto, A.

        Returns:
            tuple[Policy, dict[State, float], dict[State, dict[Action, float]]]: tuple containing the optimal policy, optimal state values and optimal action values
        """
        def action_evaluation(
                state: State,
                state_values: dict[State, float]
        ) -> dict[Action, float]:
            """Evaluate all actions at a state
            Can be interpreted as a one-step look-ahead"""

            action_values = {action: 0 for action in actions}

            if state.get_is_terminal():
                return action_values

            for action in actions:
                for state_prime, transition_probability in mdp.get_transition_matrices()[action].get_matrix()[state].items():
                    action_values[action] += (transition_probability
                                              * (state_prime.get_reward()
                                                 + gamma
                                                 * state_values[state_prime]))
            return action_values
        
        mdp = self.get_mdp()
        states = mdp.get_states()
        actions = mdp.get_actions()
        policy = self.get_policy().get_policy()
        gamma = mdp.get_gamma()

        state_values = {state: 0 for state in states}

        delta = 1

        # Value Iteration
        while delta >= self.get_theta_threshold():
            delta = 0
            for state in states:
                if state.get_is_terminal():
                    continue
                # Find the maximum value of all actions at the current state
                action_values = action_evaluation(state=state, state_values=state_values)
                best_action_value = max(action_values.values())

                # Update stopping condition
                delta = max(delta, abs(best_action_value - state_values[state]))

                # Updat value function
                state_values[state] = best_action_value

        # Get the policy
        for state in states:
            # Get best action
            action_values = action_evaluation(state=state, state_values=state_values)
            best_action_value = max(action_values.values())
            best_actions = [a for a, v in action_values.items() if v == best_action_value]

            # Greedily take the best action at the current state
            policy[state] = {act: (1/len(best_actions) if act in best_actions else 0) for act in policy[state].keys()}

        q_values = {state: 
                    action_evaluation(state=state, state_values=state_values) 
                    for state in states}
        return Policy(mdp=mdp, policy=policy), state_values, q_values

