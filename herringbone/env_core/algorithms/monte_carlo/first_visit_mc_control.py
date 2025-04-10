import numpy as np
from random import choice
from herringbone.env_core.action_space import Action
from herringbone.env_core.state_space import State
from herringbone.env_core.episode import Trajectory, Episode
from herringbone.env_core.algorithms.common import Policy
from herringbone.env_core.mdp import MDP


class MonteCarloController:
    def __init__(
            self, 
            mdp: MDP, 
            epsilon: float = 0.1,
    ):
        self.mdp = mdp
        self.epsilon = epsilon

        # Arbitrary policy
        self.policy = Policy(self.mdp)
        # Arbitrary Q(s, a)
        self.q_values: dict[State, dict[Action, float]] = {
            s: {a: 0.0 for a in mdp.get_actions()} for s in mdp.get_states()
        }
        # Keep track of the visit count for each pair
        self.N_visits: dict[tuple[State, Action], int] = {
            (s, a): 0 for s in mdp.get_states() if not s.get_is_terminal() for a in mdp.get_actions()
        }
    
    def argmax_Q(self, state: State) -> Action:
        """Returns the best action with a random tie-break."""
        q_values_state = self.q_values[state]
        max_q = max(q_values_state.values())  
        best_actions = [a for a, q in q_values_state.items() if q == max_q]
        return choice(best_actions)
    
    def update_q_values(
            self, 
            trajectory: Trajectory
    ):
        """First-visit Monte Carlo update for Q(s, a).
        
        Pseudocode adapted from: Sutton, R. S., & Barto, A. G. (2018). Reinforcement learning: An introduction (2nd ed.). The MIT Press.
        """
        S, A, R = trajectory.states, trajectory.actions, trajectory.rewards
        T = len(S) - 1 # Exclude terminal state
        G = 0
        
        for t in reversed(range(T)):
            G = self.mdp.get_gamma() * G + R[t + 1]  # Compute return
            if (S[t], A[t]) not in list(zip(S[:t], A[:t])):  # First-visit MC
                self.N_visits[S[t], A[t]] += 1
                self.q_values[S[t]][A[t]] += (1/self.N_visits[S[t], A[t]]) * (G - self.q_values[S[t]][A[t]])
                best_action = self.argmax_Q(S[t])

                for a in (actions := self.mdp.get_actions()): # epsilon greedy updating
                    if a == best_action:
                        new_prob = 1 - self.epsilon + (self.epsilon / len(actions))
                    else:
                        new_prob = self.epsilon / len(actions)

                    self.policy.update_policy_action(S[t], a, new_prob) 

    def train(
            self, 
            n_episodes: int
    ):
        """Trains a new policy for N episodes using Monte Carlo simulation."""
        for _ in range(n_episodes):
            ep = Episode(policy=self.policy, mdp=self.mdp)
            ep.run()
            self.update_q_values(ep.trajectory)
