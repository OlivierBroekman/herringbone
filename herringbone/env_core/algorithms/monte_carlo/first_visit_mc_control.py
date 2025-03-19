import numpy as np
from herringbone.env_core.action_space import Action
from herringbone.env_core.state_space import State
from herringbone.env_core.episode import Trajectory, Episode
from herringbone.env_core.algorithms.common import EpsilonGreedyPolicy, Policy
from herringbone.env_core.mdp import MDP


class MonteCarloController:
    def __init__(
            self, 
            mdp: MDP, 
            discount: float = 0.9, 
            epsilon: float = 0.1,
            seed: int = 42,
            start_coords: tuple[int, int] = (0,0)
    ):
        self.start_coords = start_coords
        self.mdp = mdp
        self.discount = discount
        self.epsilon = epsilon
        self.rng = np.random.RandomState(seed)
        

        # Arbitrary policy
        self.policy = EpsilonGreedyPolicy(self.mdp, epsilon=self.epsilon)
        # Arbitrary Q(s, a)
        self.q_values: dict[State, dict[Action, float]] = {
            s: {a: 0.0 for a in mdp.get_actions()} for s in mdp.get_states()
        }
        # Initialize Returns for every (s, a) pair with empty lists
        self.returns: dict[tuple[State, Action], list[float]] = {
            (s, a): [] for s in mdp.get_states() for a in mdp.get_actions()
        }

    def update_q_values(
            self, 
            trajectory: Trajectory
    ):
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

                for a in (actions := self.mdp.get_actions()):
                    if a == best_action:
                        new_prob = 1 - self.epsilon + (self.epsilon / len(actions))
                    else:
                        new_prob = self.epsilon / len(actions)

                    self.policy.update_policy_action(S[t], a, new_prob)
    

    def train(
            self, 
            n_episodes: int
    ):
        for _ in range(n_episodes):
            episode_seed = self.rng.randint(0, 2**31 - 1)  # Generate a new seed
            ep = Episode(policy=self.policy, mdp=self.mdp, seed=episode_seed,start_agent_coordinates=self.start_coords)
            ep.run()
            self.update_q_values(ep.trajectory)
