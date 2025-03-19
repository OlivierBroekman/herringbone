from abc import ABC, abstractmethod

from herringbone.env_core.action_space import Action
from herringbone.env_core.algorithms.common.epsilon_greedy_policy import EpsilonGreedyPolicy
from herringbone.env_core.mdp import MDP
from herringbone.env_core.state_space.piece import Piece


class TDControl(ABC):
    def __init__(
            self,
            num_episodes: int, 
            mdp: MDP,
            alpha: float = 0.5, 
            epsilon: float = 0.1, 
            gamma: float = 0.9,
    ):
        self.num_episodes = num_episodes
        self.mdp = mdp

        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma

        self.q_values = self.init_q_values()
        self.policy = EpsilonGreedyPolicy(self.mdp, epsilon, self.q_values)

    def init_q_values(self) -> dict[Piece, dict[Action, float]]:
        """Initialize all Q-values to zero."""
        return {
            state: {action: 0.0 for action in self.mdp.get_actions()}
            for state in self.mdp.get_states()
        }

    @abstractmethod
    def update_q_values(
            self,
            state: Piece, 
            action: Action,
            reward: float,
            state_prime: Piece, 
            action_prime: Action|None = None
    ) -> None:
        """Update rule to be specified by each subclass."""
        pass

    @abstractmethod
    def run(
            self
    ) -> dict[Piece, dict[Action, float]]:
        """Q-value estimation logic to be specified by each subclass."""
        pass
