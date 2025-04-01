from herringbone.env_core.mdp import MDP
from herringbone.env_core.episode import Trajectory, Episode
from herringbone.env_core.algorithms.common import Policy
import numpy as np


class MonteCarloPredictor:
    def __init__(
            self, 
            mdp: MDP, 
    ):
        self.mdp = mdp
        self.N_visits = {} # Keep track of the visit count for each state
        self.value_functions = {} # Initalise V(s) for each state
        for s in mdp.get_states():
            self.value_functions[s] = 0.0
            self.N_visits[s] = 0

    def evaluate_policy(
            self, 
            policy: Policy, 
            n_samples: int = 1000
    )-> None:
        """Runs policy evaluation for N episodes using Monte Carlo simulation."""
        for n in range(n_samples):
            ep = Episode(policy=policy, mdp=self.mdp)
            ep.run()
            self.update_value_function(ep.trajectory)
        
    def update_value_function(
            self, 
            trajectory: Trajectory
    )-> None:
        """First-visit Monte Carlo update for v_pi (s)
        
        Pseudocode adapted from: Sutton, R. S., & Barto, A. G. (2018). Reinforcement learning: An introduction (2nd ed.). The MIT Press.
        """
        S, A, R = trajectory.states, trajectory.actions, trajectory.rewards
        T = len(S) - 1 # Ignore terminal state
        G = 0
        for t in reversed(range(T)):
            G = self.mdp.get_gamma() * G + R[t + 1]  # Compute return
            if S[t] not in S[:t]:  # check if it is first time visiting the state
                self.N_visits[S[t]] += 1
                self.value_functions[S[t]] += (1/self.N_visits[S[t]]) * (G - self.value_functions[S[t]])
