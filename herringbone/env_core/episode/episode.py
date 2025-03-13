from typing import List
from herringbone.env_core.state_space import Board
from herringbone.env_core.algorithms.common import Policy
from herringbone.env_core.mdp import MDP
from dataclasses import dataclass


@dataclass
class Trajectory:
    states: List[int]
    actions: List[int]
    rewards: List[float]


class Episode:
    def __init__(
        self,
        policy: Policy,
        mdp: MDP,
        seed: int = 42,
        max_depth=1000,
        start_state=[0, 0],
    ):
        self.state = start_state
        self.reward = None
        self.trajectory: Trajectory = ([], [], [])
        self.history: List[Board]
        self.max_depth = 10000

    def run(self):
        """Runs an episode"""
        for _ in range(self.max_depth):
            self.step()

    def step(self):
        raise (NotImplementedError)
        # action = select action(state)
        self.trajectory.states.append(self.state)
        self.trajectory.actions.append(action)
        self.trajectory.actions.append(self.reward)

        # self.state, self.reward = action_result
