from herringbone.env_core.action_space import Action
from herringbone.env_core.state_space import State, Board
from herringbone.env_core.mdp import MDP
from herringbone.env_core.algorithms import Algorithm, Policy

class QIteration(Algorithm):
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
    
    def run(self) -> tuple[Policy, dict[State, dict[Action, float]]]:
        """
        Algorithm to retrieve ground truth for state-action values
        According to Bellman's Expectation Equation for (State-)Action values
        """

        def argmax_q(state: State):
            q_vals_state = q_values[state]

            max_q = max(q_vals_state.values())

            best_actions = [a for a, q in q_vals_state.items() if q == max_q]

            return best_actions[0]

        mdp = self.get_mdp()
        states = mdp.get_states()
        actions = mdp.get_actions()
        policy = self.get_policy().get_policy()
        gamma = mdp.get_gamma()
        q_values = {state: {action: 0 for action in actions} for state in states}
        
        delta = 1
        
        # Main loop
        while delta >= self.get_theta_threshold():
            delta = 0
            for state in states:
                for action in actions:
                    old_value = q_values[state][action]
                    new_value = 0
                    # Retrieve s' and p(s', r | s, a) from the environment dynamics
                    for state_prime, transition_probability in mdp.get_transition_matrices()[action].get_matrix()[state].items():
                        # Find all possible a' available in s', given by the policy
                        for action_prime, action_probability in policy[state_prime].items():
                            # Calculate new value according to Bellman Expectation for Action values
                            new_value += (transition_probability
                                            * (state.get_reward()
                                                + gamma
                                                * action_probability
                                                * q_values[state_prime][action_prime]))
                    
                    # Update q(s,a)
                    q_values[state][action] = new_value

                    # Stopping criterion
                    delta = max(delta, abs(old_value - q_values[state][action]))

        for state in states:
            # Get best action
            best_action = argmax_q(state=state)

            # Greedily take best action at current state
            policy[state] = {act: (1 if act == best_action else 0) for act in policy[state].keys()}
        
        return Policy(mdp=mdp, policy=policy), q_values