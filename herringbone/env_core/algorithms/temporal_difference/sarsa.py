from herringbone.env_core.action_space import Action
from herringbone.env_core.algorithms.common.epsilon_greedy_policy import EpsilonGreedyPolicy
from herringbone.env_core.mdp import MDP
from herringbone.env_core.state_space.piece import Piece


class Sarsa:
    def __init__(self,
        num_episodes: int, mdp: MDP,
        alpha: float = .5, epsilon: float = .1, gamma: float = .9
    ):
        self.num_episodes = num_episodes  # TODO Bram episode class?
        self.mdp = mdp

        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma

        self.q_values = self.init_q_values()
        self.policy = EpsilonGreedyPolicy(self.mdp, epsilon, self.q_values)

    def init_q_values(
        self
    ) -> dict[Piece, dict[Action, float]]:
        """Initialize all Q-values to zero."""
        return {state:
                    {action: .0 for action in self.mdp.get_actions()} for state in self.mdp.get_states()}

    def run(
        self
    ) -> dict[Piece, dict[Action, float]]:
        """Run Sarsa (on-policy-TD) to estimate Q-values."""
        for _ in range(self.num_episodes):
            state = self.mdp.get_board().pieces[0][0]  # TODO hardcoded start state
            action = self.policy.select_action(state, self.q_values)

            while not state.get_terminal():
                state_prime = self.mdp.get_board().get_state_from_action(state, action)
                reward = state_prime.get_reward()
                action_prime = self.policy.select_action(state_prime, self.q_values)

                self.q_values[state][action] += self.alpha * (
                        reward + self.gamma * self.q_values[state_prime][action_prime] - self.q_values[state][action]
                )
                state, action = state_prime, action_prime

        return self.q_values
