import numpy as np
import random
from src.env_core.action_space.action import Action
from src.env_core.state_space import Piece
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class Step:
    state: Piece
    action: Action
    reward: float

class MC_Control:
    def __init__(self, mdp, discount=0.9, epsilon=0.1):
        self.mdp = mdp
        self.discount = discount
        self.epsilon = epsilon

        # Initialize
        # Q(s, a) and returns
        self.q_values: Dict[Piece, Dict[Action, float]] = {s: {a: 0.0 for a in mdp.actions(s)} for s in mdp.states}
        self.returns: Dict[Tuple[Piece, Action], List[float]] = {} # will make later
        # arbitrray policy
        self.policy = {s: random.choice(list(self.q_values[s].keys())) for s in mdp.states}


    def update_q_values(self, history: List[Step]):
        """First-visit Monte Carlo update for Q(s, a)."""
        G = 0
        visited_pairs = set()
        for t in reversed(range(len(history))):  # Backward update (kan allebei ik weet niet wat het beste is?)
            step = history[t]
            S_t, A_t, R_t = step.state, step.action, step.reward
            G = self.discount * G + R_t  # Compute return

            if (S_t, A_t) not in visited_pairs:  # First-visit MC
                visited_pairs.add((S_t, A_t))

                if (S_t, A_t) not in self.returns: # init empty list
                    self.returns[(S_t, A_t)] = []

                self.returns[(S_t, A_t)].append(G)
                self.q_values[S_t][A_t] = np.mean(self.returns[(S_t, A_t)])

                # Policy improvement (make greedy)
                best_action = max(self.q_values[S_t], key=self.q_values[S_t].get) 
        
                self.policy[S_t] = best_action
                
                # need to understand book to finish this
                
                # episolon greedy?
                
    def train(self, n_episodes):
        for _ in range(n_episodes): 
            ep = Episode(self.policy, self.mdp)
            ep.run()
            history: List[Step] = ep.history()
            self.update_q_values(history)
        
        
# Example Usage
discount = 0.9
mc_control = MC_Control(mdp, discount)
mc_control.train(n_episodes=10000) 

optimal_policy = mc_control.policy
