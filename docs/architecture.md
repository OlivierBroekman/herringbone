## Terminology  
- state: an object on the board (e.g., agent, predator, wall, empty square).  
- board: a 2D array of states.
- reward: positive values indicate a reward, while negative values indicate a cost. Rewards are cumulative.  

## Remarks 
> [!NOTE] 
> "Colliding" with a state grants a reward; collisions are state-based, not cell-based. This allows for dynamic objects.  

- A trap is a static state that acts as a terminal state.  
- A wall is a "non-visitable" state. 

- The Policy Iteration algorithm combines both the policy evaluation and policy improvement algorithms, for simplicity's sake we will make one class algorithm (policy iteration) encapsulating both policy evaluation and policy improvement.

## Classes

### action_space  
- [x] Action (config: dict)
  * self._id: int 
  * self.type: str
  * self.directions: list[list[int]]
  * self.probabilities: list[float]
  * self.cost: int
  * self.character: str

### algorithms/common
- [x] Algorithm(ABC) (policy: Policy)
  * self.policy: Policy
  * run() -> Policy
- [x] EpsilonGreedyPolicy(Policy) (mdp: MDP, epsilon: float, policy: dict[State, dict[Action, float]])
  * self.mdp: MDP
  * self.policy: dict[State, dict[Action, float]]
  * self.epsilon: float
  * select_action(state: State, q_values: dict[State, dict[Action, float]]) -> Action
- [x] Policy (mdp: MDP, policy: dict[State, dict[Action, float]] = None)
  * self.mdp: MDP
  * self.actions: list[Actions]
  * self.board: Board
  * self.policy: dict[State, dict[Action, float]]
  * create_default_policy(actions: list[Action], board: Board) -> dict[State, dict[Action, float]]
  * update_policy_action(state: State, action: Action, probability: float)

### algorithms/dynamic_programming
- [x] PolicyIteration(Algorithm) (mdp: MDP, theta_threshold: float, gamma: float)
  * self.mdp: MDP
  * self.policy: dict[State, dict[Action, float]]
  * self.board: Board
  * self.actions: list[Action]
  * self.theta_threshold: float
  * self.gamma: float
  * run() -> tuple[Policy, dict[State, float]]
    * policy_evaluation(policy: Policy, mdp: MDP) -> dict[State, float]
    * action_evaluation(state: State, state_values: dict[State, float]) -> dict[Action, float]
- [x] ValueIteration(Algorithm) (mdp: MDP, theta_threshold: float, gamma: float)
  * self.mdp: MDP
  * self.policy: dict[State, dict[Action, float]]
  * self.board: Board
  * self.actions: list[Action]
  * self.theta_threshold: float
  * self.gamma: float
  * run() -> tuple[Policy, dict[State, float]]
    * action_evaluation(state: State, state_values: dict[State, float]) -> dict[Action, float]
  
### algorithms/monte_carlo
- [x] MonteCarloController (mdp: MDP, discount: float = 0.9, epsilon: float = 0.1, seed: int = 42, start_coords: tuple[int, int] = (0,0))
  * self.start_coords: tuple[int, int]
  * self.mdp: MDP
  * self.discount: float
  * self.epsilon: float
  * self.rng: np.RandomState
  * self.policy: EpsilonGreedyPolicy
  * self.q_values: dict[State, dict[Action, float]]
  * self.returns: dict[tuple[State, Action], list[float]]
  * update_q_values(trajectory: Trajectory)
  * train(n_episodes: int)
- [x] MonteCarloPredictor (mdp: MDP, discount: float, seed: int = 42, start_coords: tuple[int, int] = (0,0))
  * self.mdp: MDP
  * self.discount: float
  * self.returns: dict[State, list[float]] 
  * self.value_functions: dict[State, float] 
  * self.start_coords: tuple[int, int]
  * self.rng: np.RandomState
  * evaluate_policy(policy: Policy, n_samples: int = 1_000)
  * update_value_function(trajectory: Trajectory)
  
### algorithms/temporal_difference
- [x] QLearning(TDControl)
  * update_q_values(state: State, action: Action, reward: float, state_prime: State, _: None = None) -> None
  * run() -> dict[State, dict[Action, float]]
- [x] Sarsa(TDControl)
  * update_q_values(state: State, action: Action, reward: float, state_prime: State, action_prime: Action) -> None
  * run() -> dict[State, dict[Action, float]]
- [x] TDControl(ABC) (num_episodes: int, mdp: MDP, alpha: float = 0.5, epsilon: float = 0.1, gamma: float = 0.9)
  * self.num_episodes: int
  * self.mdp: MDP
  * self.alpha: float
  * self.epsilon: float
  * self.gamma: float
  * self.q_values: dict[State, dict[Action, float]]
  * self.policy: EpsilonGreedyPolicy
  * init_q_values() -> dict[State, dict[Action, float]]
  * update_q_values(state: State, action: Action, reward: float, state_prime: State, action_prime: Action|None = None) -> None
  * run() -> dict[State, dict[Action, float]]

### episode
- [x] Trajectory(dataclass)
  * states: list[State]
  * actions: list[Action]
  * rewards: list[float]
- [x] Episode (policy: Policy, mdp: MDP, seed: int = 42, max_depth: int = 1000, start_agent_coordinates: list[int] = [0,0], live_render: bool = False)
  * self.policy: Policy
  * self.mdp: MDP
  * self.live_render: bool
  * self.max_depth: int
  * self.seed: int
  * self.agent_coordinates: list[int]
  * self.trajectory: Trajectory
  * peek()
  * run()

### state_space
- [x] Color(Enum)
  * parse_color(color: str)
- [x] Board (path_config: Path, path_map: Path)
  * self.states: list[list[State]]
  * observe_states(): dict <!--Deprecated?-->
- [x] State (is_terminal: bool, location: list[int], start_location: list[int], reward: float, character: str, color: str)
  * self.is_terminal: bool
  * self.location: list[int]
  * self.reward: float
  * self.color: str

### transition_space
- [x] TransitionMatrix (mdp: MDP, action: Action)
  * self.mdp: MDP
  * self.action: Action
  * self.matrix: dict[State, dict[State, float]]
  * build_transition_matrix(board: Board, action: Action) -> dict[State, dict[State, float]]
  * get_successor_state(state: State) -> dict[State, float]

### utils
- [x] map_loader
  * load_config(path_config: Path) -> dict
  * read_map(path_map) -> list[list[int]]
  * init_state(state_vals: dict[str, Any], coordinates: list[int]) -> State
  * load_map(path_config: Path, path_map: Path) -> list[list[State]]

- [x] MDP (actions: list[Action], board: Board, transition_matrices: dict[Action, TransitionMatrix] = None)
  * self.actions: list[Actions]
  * self.board: Board
  * self.transition_matrices: dict[Action, TransitionMatrix]


## Directory Tree
```
.
├── demo.ipynb
├── docs
│   ├── algorithms.md
│   ├── architecture.md
│   ├── CONTRIBUTING.md
│   ├── customization.md
│   └── roadmap.md
├── herringbone
│   ├── env_core
│   │   ├── action_space
│   │   │   ├── action.py
│   │   │   └── __init__.py
│   │   ├── algorithms
│   │   │   ├── common
│   │   │   │   ├── algorithm.py
│   │   │   │   ├── epsilon_greedy_policy.py
│   │   │   │   ├── __init__.py
│   │   │   │   └── policy.py
│   │   │   ├── dynamic_programming
│   │   │   │   ├── __init__.py
│   │   │   │   ├── policyiteration.py
│   │   │   │   └── valueiteration.py
│   │   │   ├── __init__.py
│   │   │   ├── monte_carlo
│   │   │   │   ├── first_visit_mc_control.py
│   │   │   │   ├── first_visit_mc_prediction.py
│   │   │   │   └── __init__.py
│   │   │   └── temporal_difference
│   │   │       ├── deep_q_learning.py
│   │   │       ├── __init__.py
│   │   │       ├── q_learning.py
│   │   │       ├── sarsa.py
│   │   │       ├── td_control.py
│   │   │       └── td_zero.py
│   │   ├── config
│   │   │   ├── action_config.json
│   │   │   └── state_config.json
│   │   ├── episode
│   │   │   ├── episode.py
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── maps
│   │   │   ├── danger_holes.csv
│   │   │   ├── double_fish.csv
│   │   │   ├── easy.csv
│   │   │   ├── example2.csv
│   │   │   ├── example.csv
│   │   │   ├── flappy_bird.csv
│   │   │   ├── gamma.csv
│   │   │   ├── heart.csv
│   │   │   ├── maze.csv
│   │   │   ├── mega.csv
│   │   │   ├── slides.csv
│   │   │   └── wall_of_death.csv
│   │   ├── mdp.py
│   │   ├── state_space
│   │   │   ├── board.py
│   │   │   ├── __init__.py
│   │   │   └── state.py
│   │   ├── transition_space
│   │   │   ├── __init__.py
│   │   │   └── transition_matrix.py
│   │   └── utils
│   │       ├── actions_loader.py
│   │       ├── color.py
│   │       ├── config_loader.py
│   │       ├── __init__.py
│   │       ├── map_loader.py
│   │       └── render.py
│   ├── __init__.py
│   └── tests
│       ├── _init_algorithms.py
│       └── __init__.py
├── LICENSE
├── README.md
└── requirements.txt

17 directories, 60 files
```
