from typing import override

from herringbone.env_core.action_space import Action
from herringbone.env_core.algorithms.temporal_difference.td_control import TDControl
from herringbone.env_core.state_space.state import State


class Sarsa(TDControl):
    @override
    def update_q_values(
        self,
        state: State,
        action: Action,
        state_prime: State,
        action_prime: Action,
    ) -> None:
        """
        Update the Q-value function for a certain state-action pair using the Sarsa update rule.

        Pseudocode adapted from: Sutton, R. S., & Barto, A. G. (2018). Reinforcement learning: An introduction (2nd ed.). The MIT Press.
        """
        self.q_values[state][action] += self.alpha * (
            self.reward_last
            + self.mdp.get_gamma() * self.q_values[state_prime][action_prime]
            - self.q_values[state][action]
        )

    @override
    def run(self) -> dict[State, dict[Action, float]]:
        """
        Estimate the Q-value function for a given policy using Sarsa.

        Pseudocode adapted from: Sutton, R. S., & Barto, A. G. (2018). Reinforcement learning: An introduction (2nd ed.). The MIT Press.
        """
        for _ in range(self.num_episodes):
            state = self.mdp.get_start_state()
            action = self.policy.get_next_action(state, self.q_values)

            while not state.get_is_terminal():
                state_prime = self.mdp.get_next_state(state, action)
                self.reward_last = state_prime.get_reward()
                action_prime = self.policy.get_next_action(state_prime, self.q_values)
                self.update_q_values(state, action, state_prime, action_prime)
                state, action = state_prime, action_prime

            self.decay_epsilon()

        return self.q_values
