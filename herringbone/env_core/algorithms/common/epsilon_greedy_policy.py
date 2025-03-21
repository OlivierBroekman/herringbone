from random import random, choice

from herringbone.env_core.action_space.action import Action
from herringbone.env_core.mdp import MDP
from herringbone.env_core.algorithms.common.policy import Policy
from herringbone.env_core.state_space.state import State


class EpsilonGreedyPolicy(Policy):
    def __init__(
        self,
        mdp: MDP,
        epsilon: float,
        policy: dict[State, dict[Action, float]] = None
    ):
        super().__init__(mdp, policy)
        self.epsilon = epsilon

    def get_next_action(
        self,
        state: State,
        q_values: dict[State, dict[Action, float]]
    ) -> Action:
        actions = list(q_values[state].keys())
        if random() < self.epsilon:
            return choice(actions)  
        else:
            max_q_value = max(q_values[state].values())
            best_actions = [a for a in actions if q_values[state][a] == max_q_value]
            
            # Randomly choose one of the best actions if there's a tie
            return choice(best_actions)
