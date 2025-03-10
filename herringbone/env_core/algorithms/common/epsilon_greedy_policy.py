from random import random, choice

from herringbone.env_core.action_space.action import Action
from herringbone.env_core.mdp import MDP
from herringbone.env_core.algorithms.common.policy import Policy
from herringbone.env_core.state_space.piece import Piece


class EpsilonGreedyPolicy(Policy):
    def __init__(self,
        mdp: MDP,
        epsilon: float,
        policy: dict[Piece, dict[Action, float]] = None
    ):
        super().__init__(mdp, policy)
        self.epsilon = epsilon

    def select_action(self,
        state: Piece,
        q_values: dict[Piece, dict[Action, float]]
    ) -> Action:
        actions = list(q_values[state].keys())
        return choice(actions) if random() < self.epsilon else max(actions, key=lambda action: q_values[state][action])
