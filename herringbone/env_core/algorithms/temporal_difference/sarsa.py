from typing import override

from herringbone.env_core.action_space import Action
from herringbone.env_core.algorithms.temporal_difference.td_control import TDControl
from herringbone.env_core.state_space.piece import Piece


class Sarsa(TDControl):
    @override
    def update_q_values(
        self,
        state: Piece, action: Action,
        reward: float,
        state_prime: Piece, action_prime: Action,
    ) -> None:
        """Sarsa update rule."""
        self.q_values[state][action] += self.alpha * (
            reward + self.gamma * self.q_values[state_prime][action_prime] - self.q_values[state][action]
        )

    @override
    def run(self) -> dict[Piece, dict[Action, float]]:
        """Run Sarsa (on-policy-TD) to estimate Q-values."""
        for _ in range(self.num_episodes):
            state = self.mdp.get_board().pieces[0][0]  # TODO hardcoded
            action = self.policy.select_action(state, self.q_values)

            while not state.get_terminal():
                state_prime = self.mdp.get_board().get_state_from_action(state, action)  # TODO via transition matrix
                reward = state_prime.get_reward()
                action_prime = self.policy.select_action(state_prime, self.q_values)

                self.update_q_values(state, action, reward, state_prime, action_prime)

                state, action = state_prime, action_prime

        return self.q_values
