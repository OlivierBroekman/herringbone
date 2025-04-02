import sys
from collections import namedtuple, deque
from typing import override

import random
import torch
from torch import nn
import torch.nn.functional as F

from herringbone.env_core.mdp import MDP
from herringbone.env_core.state_space.state import State
from herringbone.env_core.action_space.action import Action
from herringbone.env_core.algorithms.temporal_difference.q_learning import QLearning


class DeepQNetwork(nn.Module):
    """
    Code adapted from: Paszke, A. & Towers, M. (2024). Reinforcement Learning (DQN) Tutorial. PyTorch. https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
    """

    def __init__(self, num_states: int, num_actions: int):
        super().__init__()
        self.fc1 = nn.Linear(num_states, num_states)
        self.fc2 = nn.Linear(num_states, num_actions)

    def forward(self, x) -> torch.Tensor:
        x = F.relu(self.fc1(x))
        return self.fc2(x)


Transition = namedtuple("Transition", ("state", "action", "state_prime", "reward"))


class ReplayMemory:
    """
    Code adapted from: Paszke, A. & Towers, M. (2024). Reinforcement Learning (DQN) Tutorial. PyTorch. https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
    """

    def __init__(self, capacity: int):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        self.memory.append(Transition(*args))

    def sample(self, batch_size: int):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

    def __iter__(self):
        return iter(self.memory)


class DeepQLearning(QLearning):
    """
    Code adapted from: JohnnyCode. (2023). Deep Q-Learning/Deep Q-Network (DQN) Explained | Python Pytorch Deep Reinforcement Learning. YouTube. https://www.youtube.com/watch?v=EUrWGTCGzlA
    Pseudocode adapted from: Mnih, V., Kavukcuoglu, K., Silver, D., Graves, A., Antonoglou, I., Wierstra, D., & Riedmiller, M. (2013). Playing Atari with Deep Reinforcement Learning. arXiv. https://arxiv.org/pdf/1312.5602
    """

    SYNC_RATE = 10
    REPLAY_MEMORY_SIZE = 1_000
    MINI_BATCH_SIZE = 32
    DEPTH_MAX = 5_000

    LOSS_FN = nn.MSELoss()
    OPTIMIZER = torch.optim.AdamW

    def __init__(
        self,
        num_episodes: int,
        mdp: MDP,
        alpha: float = 0.5,
        epsilon: float = 1.0,
        epsilon_min: float = sys.float_info.epsilon,
        epsilon_delta: float = 0.01,
        reward_threshold: float = 1.0,
        reward_increment: float = 1.0,
    ):
        super().__init__(
            num_episodes=num_episodes,
            mdp=mdp,
            alpha=alpha,
            epsilon=epsilon,
            epsilon_min=epsilon_min,
            epsilon_delta=epsilon_delta,
            reward_threshold=reward_threshold,
            reward_increment=reward_increment,
        )
        torch.manual_seed(self.mdp.seed)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.states = self.mdp.get_states()
        self.num_states = len(self.states)
        self.actions = self.mdp.get_actions()
        self.num_actions = len(self.actions)

        self.dqn_policy = DeepQNetwork(
            num_states=self.num_states,
            num_actions=self.num_actions,
        )
        self.dqn_target = DeepQNetwork(
            num_states=self.num_states,
            num_actions=self.num_actions,
        )
        self.dqn_target.load_state_dict(self.dqn_policy.state_dict())

        self.memory = ReplayMemory(self.REPLAY_MEMORY_SIZE)
        self.optimizer = self.OPTIMIZER(
            self.dqn_policy.parameters(), lr=1e-4, amsgrad=True
        )

    @override
    def run(self) -> dict[State, dict[Action, float]]:
        """
        Train the DQN agent to estimate the Q-function.
        """
        step_count = 0

        for _ in range(self.num_episodes):

            # Initialize finite sequence of actions and observations (preprocessing absent)
            state = self.mdp.get_start_state()

            while not state.get_is_terminal() and step_count < self.DEPTH_MAX:

                # With probability ε select random action a_t
                if random.random() < self.epsilon:
                    action = random.choice(self.actions)

                # Otherwise select a_t = max_a Q*(s_t, a; θ)
                else:
                    with torch.no_grad():
                        q_values = self.dqn_policy(self.get_state_vector(state)).to(
                            self.device
                        )
                        action = self.actions[
                            random.choice(
                                torch.nonzero(q_values == q_values.max())
                                .squeeze()
                                .cpu()
                                .numpy()
                                .flatten()
                            )
                        ]

                # Execute action a_t in emulator and observe reward r_t and s_{t+1}
                state_prime = self.mdp.get_next_state(state, action)
                self.reward_last = state_prime.get_reward()

                # Store transition (s_t, a_t, r_t, s_{t+1}) in replay memory
                self.memory.push(state, action, state_prime, self.reward_last)
                self.rewards.append(self.reward_last)  # For analysis
                state = state_prime
                step_count += 1

            # Sample random mini-batch of transitions (s_j, a_j, r_j, s_{j+1}) from replay memory
            if len(self.memory) > self.MINI_BATCH_SIZE and any(
                trans.state_prime.get_is_terminal() for trans in self.memory
            ):
                mini_batch = self.memory.sample(self.MINI_BATCH_SIZE)
                self.optimize(mini_batch)
                self.decay_epsilon()

                # Periodically update the target net with the current policy weights
                if step_count > self.SYNC_RATE:
                    self.dqn_target.load_state_dict(self.dqn_policy.state_dict())
                    step_count = 0

        # torch.save(self.dqn_policy.state_dict(), "dqn_policy.pt")
        self.__set_q_values(self.dqn_policy)

        return self.q_values

    def optimize(
        self, mini_batch: list[Transition[State, Action, State, float]]
    ) -> None:
        """
        Update the DQN policy using a mini-batch of transitions.
        """
        q_list_curr = []
        q_list_target = []

        for state, action, state_prime, reward in mini_batch:

            # Set y_j to r_j for terminal s_{j+1}
            if state_prime.get_is_terminal():
                target = torch.tensor([reward], dtype=torch.float).to(self.device)

            # Set y_j to r_j + γ max_{a'} Q(s_{j+1}, a'; θ) for non-terminal s_{j+1}
            else:
                with torch.no_grad():
                    target = (
                        (
                            reward
                            + self.mdp.gamma
                            * self.dqn_target(self.get_state_vector(state_prime)).max()
                        )
                        .clone()
                        .detach()
                    )

            # Get the current Q-value according to the policy net
            q_curr = self.dqn_policy(self.get_state_vector(state)).to(self.device)
            q_list_curr.append(q_curr)

            # Get the current target Q-value according to the target net (Bellman)
            q_target = self.dqn_target(self.get_state_vector(state)).to(self.device)
            q_target[action.get_id()] = target
            q_list_target.append(q_target)

        # Perform a gradient descent step on (y_j - Q(s_j, a_j; θ))^2
        loss = self.LOSS_FN(torch.stack(q_list_curr), torch.stack(q_list_target))
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def get_state_vector(self, state: State) -> torch.Tensor:
        """
        Represent a state as one-hot encoded vector.
        """
        input_tensor = torch.zeros(self.num_states).to(self.device)
        input_tensor[state.idx] = 1

        return input_tensor

    def __set_q_values(self, dqn: nn.Module) -> None:
        """
        Set Q-value table for display.
        """
        for s in self.states:
            q = dqn(self.get_state_vector(s).to(self.device)).detach().cpu().numpy()
            self.q_values[s] = {
                a: 0 if s.get_is_terminal() else q[a_idx]
                for a_idx, a in enumerate(self.actions)
            }
