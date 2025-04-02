from typing import override

from herringbone.env_core.action_space import Action
from herringbone.env_core.algorithms.temporal_difference.td_control import TDControl
from herringbone.env_core.state_space.state import State


class QLearning(TDControl):
    @override
    def update_q_values(
        self, state: State, action: Action, state_prime: State, _: None = None
    ) -> None:
        """
        Update the Q-value function for a certain state-action pair using the Q-learning update rule.

        Pseudocode adapted from: Sutton, R. S., & Barto, A. G. (2018). Reinforcement learning: An introduction (2nd ed.). The MIT Press.
        """
        
        action_max = max(self.q_values[state_prime], key=self.q_values[state_prime].get)

        self.q_values[state][action] += self.alpha * (
            self.reward_last
            + self.mdp.get_gamma() * self.q_values[state_prime][action_max]
            - self.q_values[state][action]
        )

    @override
    def run(self) -> dict[State, dict[Action, float]]:
        """
        Estimate the optimal Q-value function using Q-learning.

        Pseudocode adapted from: Sutton, R. S., & Barto, A. G. (2018). Reinforcement learning: An introduction (2nd ed.). The MIT Press.
        """
        
        # Loop for each episode
        for _ in range(self.num_episodes):

            # Initialize S
            state = self.mdp.get_start_state()

            # Loop for each step of episode until S is terminal
            while not state.get_is_terminal():

                # Choose A from S using policy derived from Q (e.g., epsilon-greedy)
                action = self.policy.get_next_action(state, self.q_values)

                # Take action A, observe S', R
                state_prime = self.mdp.get_next_state(state, action)
                self.reward_last = state_prime.get_reward()
                self.rewards.append(self.reward_last)  # For analysis

                # Q(S, A) ← A(S, A) + α[R + γ max_a Q(S', a) - Q(S, A)]
                self.update_q_values(state, action, state_prime)

                # S ← S'
                state = state_prime

            self.decay_epsilon()

        return self.q_values
