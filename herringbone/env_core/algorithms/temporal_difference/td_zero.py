from herringbone.env_core.algorithms.common.policy import Policy


class TDZero:
    def __init__(
        self,
        num_episodes: int,
        policy: Policy,
        alpha: float = 0.5,
        gamma: float = 0.9,
    ):
        self.num_episodes = num_episodes
        self.policy = policy
        self.alpha = alpha
        self.gamma = gamma
        self.state_values = {state: 0 for state in self.policy.get_mdp().get_states()}

    def update_value_function(self, state, reward, state_prime):
        """
        Update the value function for a certain state using the TD(0) learning update rule.

        Pseudocode adapted from: Sutton, R. S., & Barto, A. G. (2018). Reinforcement learning: An introduction (2nd ed.). The MIT Press.
        """
        self.state_values[state] += self.alpha * (
            reward
            + self.gamma * self.state_values[state_prime]
            - self.state_values[state]
        )

    def run(self):
        """
        Estimate the value function for a given policy using Tabular TD(0).

        Pseudocode adapted from: Sutton, R. S., & Barto, A. G. (2018). Reinforcement learning: An introduction (2nd ed.). The MIT Press.
        """
        for _ in range(self.num_episodes):
            state = self.policy.get_mdp().start_state

            while not state.get_is_terminal():
                action = self.policy.get_next_action(state, self.policy.get_policy())

                state_prime = max(  # TODO duplicate (3) code
                    self.policy.get_mdp()
                    .get_transition_matrices()[action]
                    .get_matrix()[state]
                    .items(),
                    key=lambda state_prob_pair: state_prob_pair[1],
                )[0]

                reward = state_prime.get_reward()
                self.update_value_function(state, reward, state_prime)
                state = state_prime

        return self.state_values
