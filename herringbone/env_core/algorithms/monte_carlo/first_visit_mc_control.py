import numpy as np
from herringbone.env_core.action_space import Action
from herringbone.env_core.state_space import Piece
from herringbone.env_core.episode import Trajectory, Episode
from herringbone.env_core.algorithms.common import EpsilonGreedyPolicy, Policy
from herringbone.env_core.mdp import MDP
from typing import List, Dict, Tuple


class MonteCarloController:
    def __init__(self, mdp: MDP, discount=0.9, epsilon=0.1, seed=42):
        self.mdp = mdp
        self.discount = discount
        self.epsilon = epsilon
        self.rng = np.random.RandomState(seed)
        

        # Arbitrary policy
        self.policy = EpsilonGreedyPolicy(self.mdp, epsilon=self.epsilon)
        # Arbitrary Q(s, a)
        self.q_values: Dict[Piece, Dict[Action, float]] = {
            s: {a: 0.0 for a in mdp.get_actions(s)} for s in mdp.get_states()
        }
        # Initialize Returns for every (s, a) pair with empty lists
        self.returns: Dict[Tuple[Piece, Action], List[float]] = {
            (s, a): [] for s in mdp.get_states() for a in mdp.get_actions(s)
        }

    def update_q_values(self, trajectory: Trajectory):
        """First-visit Monte Carlo update for Q(s, a)."""
        S, A, R = trajectory.states, trajectory.actions, trajectory.rewards
        T = len(S)
        G = 0
        for t in reversed(range(T - 1)):
            G = self.discount * G + R[t + 1]  # Compute return
            if (S[t], A[t]) not in list(zip(S[:t], A[:t])):  # First-visit MC

                self.returns[(S[t], A[t])].append(G)
                self.q_values[S[t]][A[t]] = np.mean(self.returns[(S[t], A[t])])  #

                best_action = max(
                    self.q_values[S[t]], key=self.q_values[S[t]].get
                )  # argmax_a Q(S_t,a)

                for a in (actions := self.mdp.get_actions(S[t])):
                    if a == best_action:
                        new_prob = 1 - self.epsilon + (self.epsilon / len(actions))
                    else:
                        new_prob = self.epsilon / len(actions)

                    self.policy.update_policy_action(S[t], a, new_prob)
    

    def train(self, n_episodes):
        for _ in range(n_episodes):
            episode_seed = self.rng.randint(0, 2**32 - 1)  # Generate a new seed
            ep = Episode(policy=self.policy, mdp=self.mdp, seed=episode_seed)
            ep.run()
            trajectory = ep.trajectory()
            self.update_q_values(trajectory)
