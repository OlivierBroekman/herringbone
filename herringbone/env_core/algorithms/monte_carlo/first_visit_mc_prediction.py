from herringbone.env_core.mdp import MDP
from herringbone.env_core.episode import Trajectory, Episode
from herringbone.env_core.algorithms.common import Policy
import numpy as np


class MonteCarloPredictor:
    # initialize
    # V(s) for all s in States
    # Returns(S) <- an empty list for all s in S(t)

    def __init__(
            self, 
            mdp: MDP, 
    ):
        self.mdp = mdp
        self.N = {}
        self.value_functions = {}
        for s in mdp.get_states():
            self.value_functions[s] = 0.0
            self.N[s] = 0

    # input: policy
    def evaluate_policy(
            self, 
            policy: Policy, 
            n_samples: int = 1000
    )-> None:
        """Runs policy evaluation using Monte Carlo simulation."""
        for n in range(n_samples):
            ep = Episode(policy=policy, mdp=self.mdp)
            ep.run()
            self.update_value_function(ep.trajectory)
        
    def update_value_function(
            self, 
            trajectory: Trajectory
    )-> None:
        """First-visit Monte Carlo update for V"""
        S, A, R = trajectory.states, trajectory.actions, trajectory.rewards
        T = len(S) - 1 # Drop terminal state
        G = 0
        for t in reversed(range(T)):
            G = self.mdp.get_gamma() * G + R[t + 1]  # Compute return
            if S[t] not in S[:t]:  # check if it is first time visiting the state
                self.N[S[t]] += 1
                self.value_functions[S[t]] = self.value_functions[S[t]] + (1/self.N[S[t]]) * (G - self.value_functions[S[t]])
