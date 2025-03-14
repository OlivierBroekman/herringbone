from herringbone.env_core.mdp import MDP
from herringbone.env_core.episode import Trajectory, Episode
from herringbone.env_core.algorithms.common import Policy
import numpy as np


class MonteCarloPredictor:
    # initialize
    # V(s) for all s in States
    # Returns(S) <- an empty list for all s in S(t)

    def __init__(self, mdp: MDP, discount: float, seed=42, start_coords=(0,0)):
        self.mdp = mdp
        self.discount = discount
        self.returns = {}
        self.value_functions = {}
        self.start_coords = start_coords
        self.rng = np.random.RandomState(seed)
        for s in mdp.get_states():
            self.value_functions[s] = 0
            self.returns[s] = []

    # input: policy
    def evaluate_policy(self, policy: Policy, n_samples=1000):
        """Runs policy evaluation using Monte Carlo simulation."""
        for n in range(n_samples):
            episode_seed = self.rng.randint(0, 2**31 - 1)  # Generate a new seed
            ep = Episode(policy=policy, mdp=self.mdp, seed=episode_seed, start_agent_coordinates=self.start_coords)
            ep.run()
            self.update_value_function(ep.trajectory)

    def update_value_function(self, trajectory: Trajectory):
        """First-visit Monte Carlo update for V"""
        S, A, R = trajectory.states, trajectory.actions, trajectory.rewards
        T = len(S)
        G = 0
        for t in reversed(range(T - 1)):
            G = self.discount * G + R[t + 1]
            if S[t] not in S[:t]:  # check if it is first time visiting the state
                self.returns[S[t]].append(G)
                self.value_functions[S[t]] = np.mean(self.returns[S[t]])
