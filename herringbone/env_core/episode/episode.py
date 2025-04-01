from herringbone.env_core.state_space import Board, State
from herringbone.env_core.algorithms.common import Policy
from herringbone.env_core.mdp import MDP
from herringbone.env_core.action_space import Action
from herringbone.env_core.utils import Render
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
        live_render: bool = False
    ):
        # Problem Space
        self.policy = policy
        self.mdp = mdp
        self.live_render = live_render
        
        # Settings
        self.max_depth = max_depth
    
        # Innitalisation
        self.trajectory: Trajectory = Trajectory([], [], [])

    def peek(
            self, render_mode: str = "rewards"
    ):
        Render.preview_frame(board=self.mdp.get_board(), agent_state=None, render_mode=render_mode)
        
    def run(
            self, live_render = None
    )-> None:
        """Runs an episode"""
        depth = 0
        state = self.mdp.get_start_state()
        self.trajectory.states.append(state)
        reward = float('nan') # No reward in initial state
        self.trajectory.rewards.append(reward)
        while not state.get_is_terminal() and depth < self.max_depth:
            # Select action
            action = self.policy.get_next_action(state, self.policy.get_policy())
            self.trajectory.actions.append(action)

            # Render current (s, a, r) state
            if live_render:
                Render.preview_frame(self.mdp.get_board(), state,render_mode=live_render,action=action,t=depth)
        
            # update state
            state = self.mdp.get_next_state(state, action)
            self.trajectory.states.append(state)
            
            # Update reward
            reward = state.get_reward()
            self.trajectory.rewards.append(reward)
            
            depth += 1
            
        # Render terminal frame   
        if live_render:
                Render.preview_frame(self.mdp.get_board(), state,render_mode=live_render,action=None,t=depth)
 
    