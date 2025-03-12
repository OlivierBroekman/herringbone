from typing import override

from herringbone.env_core.action_space import Action
from herringbone.env_core.algorithms.temporal_difference.td_control import TDControl
from herringbone.env_core.state_space.piece import Piece


class QLearning(TDControl):
    @override
    def update_q_values(
        self,
        state: Piece, action: Action,
        reward: float,
        state_prime: Piece, _: None=None
    ) -> None:
        """Q-learning update rule."""
        action_max = max(self.q_values[state_prime], key=self.q_values[state_prime].get)

        self.q_values[state][action] += self.alpha * (
            reward + self.gamma * self.q_values[state_prime][action_max]- self.q_values[state][action]
        )

    @override
    def run(self) -> dict[Piece, dict[Action, float]]:
        """Run Q-learning (off-policy TD) to estimate Q-values."""
        for _ in range(self.num_episodes):
            state = self.mdp.get_board().pieces[0][0]  # TODO hardcoded

            while not state.get_terminal():
                action = self.policy.select_action(state, self.q_values)
                state_prime = max(
                    self.mdp.get_transition_matrices()[action].get_matrix()[state].items(),
                    key=lambda state_prob_pair: state_prob_pair[1]
                )[0]
                reward = state_prime.get_reward()

                self.update_q_values(state, action, reward, state_prime)

                state = state_prime

        return self.q_values
