from herringbone.env_core.state_space import Board, Piece
from herringbone.env_core.algorithms.common import Policy
from herringbone.env_core.mdp import MDP
from herringbone.env_core.action_space import Action
from dataclasses import dataclass
import random

@dataclass
class Trajectory:
    states: list[Piece]
    actions: list[Action]
    rewards: list[float]


class Episode:
    def __init__(
        self,
        policy: Policy,
        mdp: MDP,
        seed: int = 42,
        max_depth: int = 1000,
        start_agent_coordinates: list[int] = [0, 0],
        live_render: bool = False
    ):
        # Problem Space
        self.policy = policy
        self.mdp = mdp
        self.live_render = live_render
        
        # Settings
        self.max_depth = max_depth
        self.seed = seed
        random.seed(self.seed)

     
        # Innitalisation
        self.agent_coordinates = start_agent_coordinates # another name? agent_coords does not really solve the length issue.
        self.trajectory: Trajectory = Trajectory([], [], [])

    def peek(
            self
    ):
        print(self.mdp.get_board())
        
    def run(
            self
    ):
        """Runs an episode"""
        
        depth = 0
        state = self.mdp.get_board().pieces[self.agent_coordinates[0]][self.agent_coordinates[1]]
        reward = None
        action = None
        while not state.get_is_terminal() and depth < self.max_depth:
            #TODO: REMOVE DEBUG
            # print(f"t: {depth} | S{state}, R:{reward}, A:{action}" ) 
            if self.live_render:
                pass
               # utils.render(board, coords)
            
            # Select action
            #action = self.policy.select_action(state, self.q_values)
            action = self.policy.select_action(state, self.policy.get_policy())
            
        
            # Get new state
            state_prime = max(
                self.mdp.get_transition_matrices()[action].get_matrix()[state].items(),
                key=lambda state_prob_pair: state_prob_pair[1]
            )[0]
            
            # Update reward
            reward = state_prime.get_reward()
            
             # Update trajectory
            self.trajectory.states.append(state)
            self.trajectory.actions.append(action)
            self.trajectory.rewards.append(reward)
            
            # Update state
            state = state_prime

            depth += 1   
            
            

    