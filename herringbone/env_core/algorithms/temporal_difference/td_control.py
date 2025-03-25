from abc import ABC, abstractmethod
import sys

from herringbone.env_core.action_space import Action
from herringbone.env_core.algorithms.common.epsilon_greedy_policy import (
    EpsilonGreedyPolicy,
)
from herringbone.env_core.mdp import MDP
from herringbone.env_core.state_space.state import State


class TDControl(ABC):
    def __init__(
        self,
        num_episodes: int,
        mdp: MDP,
        alpha: float = 0.5,
        epsilon: float = 1.0,
        epsilon_min: float = sys.float_info.epsilon,
        epsilon_delta: float = 0.01,
        reward_threshold: float = 1.0,
        reward_increment: float = 1.0,
        gamma: float = 0.9,
    ):
        self.num_episodes = num_episodes
        self.mdp = mdp
        self.alpha = alpha

        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_delta = epsilon_delta
        self.reward_last = 0.0
        self.reward_threshold = reward_threshold
        self.reward_increment = reward_increment

        self.gamma = gamma

        self.q_values = self.init_q_values()
        self.policy = EpsilonGreedyPolicy(self.mdp, epsilon, self.q_values)

    def init_q_values(self) -> dict[State, dict[Action, float]]:
        """Initialize all Q-values to zero."""
        return {
            state: {action: 0.0 for action in self.mdp.get_actions()}
            for state in self.mdp.get_states()
        }

    @abstractmethod
    def update_q_values(
        self,
        state: State,
        action: Action,
        state_prime: State,
        action_prime: Action | None = None,
    ) -> None:
        """Update rule to be specified by each subclass."""
        pass

    @abstractmethod
    def run(self) -> dict[State, dict[Action, float]]:
        """Q-value estimation logic to be specified by each subclass."""
        pass

    def decay_epsilon(self):
        """
        Decay epsilon using Reward-Based Epsilon Decay.

        Pseudocode adapted from: Maroti, A. (2019). Reward Based Epsilon Decay: An exploration strategy based on agent's learning abilities. https://aakash94.github.io/Reward-Based-Epsilon-Decay/
        """
        if (
            self.epsilon > self.epsilon_min
            and self.reward_last >= self.reward_threshold
        ):
            self.epsilon = max(self.epsilon - self.epsilon_delta, self.epsilon_min)
            self.reward_threshold += self.reward_increment
