from herringbone.env_core.state_space import Board, State
from herringbone.env_core.algorithms.common import Policy
from herringbone.env_core.mdp import MDP
from herringbone.env_core.action_space import Action
from dataclasses import dataclass
import random



@dataclass
class Trajectory:
    states: list[State]
    actions: list[Action]
    rewards: list[float]


class Episode:
    def __init__(
        self,
        policy: Policy,
        mdp: MDP,
        max_depth: int = 10000,
        start_agent_coordinates: list[int] = [0, 0],
        live_render: bool = False
    ):
        # Problem Space
        self.policy = policy
        self.mdp = mdp
        self.live_render = live_render
        
        # Settings
        self.max_depth = max_depth
    

     
        # Innitalisation
        self.agent_coordinates = start_agent_coordinates # another name? agent_coords does not really solve the length issue.
        self.trajectory: Trajectory = Trajectory([], [], [])

    def peek(
            self
    ):
        print(self.mdp.get_board())
        
    def run(
            self, live_render = None
    ):
        """Runs an episode"""
        
        depth = 0
        state = self.mdp.get_board().states[self.agent_coordinates[0]][self.agent_coordinates[1]]
        reward = float('nan') # No reward in initial state
        self.trajectory.rewards.append(reward)
        while not state.get_is_terminal() and depth < self.max_depth:
            
            # Select action
            action = self.policy.get_next_action(state, self.policy.get_policy())
            self.trajectory.actions.append(action)
                     
            if live_render:
                print(f"t: {depth} | S: {state}, R: {reward}, A: {action}" ) 
        
            
            # Get new state
            state_prime = max(
                self.mdp.get_transition_matrices()[action].get_matrix()[state].items(),
                key=lambda state_prob_pair: state_prob_pair[1]
            )[0]
            
            # add old state to trajectory
            self.trajectory.states.append(state)

            # Update state
            state = state_prime
            
            # Update reward
            reward = state_prime.get_reward()
            self.trajectory.rewards.append(reward)
            
            depth += 1   

 
    