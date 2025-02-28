from src.env_core.action_space.action import Action
from src.env_core.state_space import Piece
from dataclasses import dataclass
from typing import List
from src.env_core.mdp import MDP
from src.env_core.episode.policy import Policy
from src.env_core.episode.episode import Episode
import numpy as np

#TODO: MDP.
#TODO: policy
#TODO: unpacken.

@dataclass
class Step:
    state: Piece
    action: Action 
    reward: float


class MC_pred():
    # initialize
    # V(s) for all s in States
    # Returns(S) <- an empty list for all s in S(t)
    # waarom gebruik ik een MDP?? is dat legaal!
    
    def __init__(self, mdp: MDP, discount: float):
        self.mdp = mdp
        self.discount = discount
        self.returns = {}
        self.value_functions = {}
        for s in mdp.states: # mdp.get_board().get_states() # UNPACKEN
            self.value_functions[s] = 0
            self.returns[s] = [] 
          
    # input: policy         
    def evaluate_policy(self, policy: Policy, n_samples=1000):
        """Runs policy evaluation using Monte Carlo simulation."""
        for n in range(n_samples):
            ep = Episode(policy, self.mdp)
            ep.run()
            history: List[Step] = ep.history()   # history -> [(S0, A0, R1),(S1, A1, R2)] ( List of (state, action, reward))
            self.update_value_function(history) 
      
    
    def update_value_function(self, history: List[Step]):
        """First-visit Monte Carlo update for V"""
        G = 0
        visited_states = set()
        for t in enumerate(history[:-1]): # stop at second last step / don't include terminal state 
            S_t = history[t].state
            R_t_plus_1 = history[t + 1].reward  # does this make sense?
            G = self.discount * G + R_t_plus_1  
            if S_t not in visited_states: # check if we are first visiting the state
                visited_states.add(S_t)
                self.returns[S_t].append(G)
                self.value_functions[S_t] = np.mean(self.returns[S_t])

     

### main 
discount = 1
mc_predictor = MC_pred(mdp, discount)
mc_predictor.evaluate_policy(policy, n_samples=1000
    

### episode
class Episode():
    MDP = 0
    policy = 0
    def run():
        for i in range(depth):
            self.step()