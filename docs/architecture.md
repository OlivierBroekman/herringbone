## Terminology  
- piece: an object on the board (e.g., agent, predator, wall, empty square).  
- board: a 2D array of pieces.
- reward: positive values indicate a reward, while negative values indicate a cost. Rewards are cumulative.  

## Remarks 
> [!NOTE] 
> "Colliding" with a piece grants a reward; collisions are piece-based, not cell-based. This allows for dynamic objects.  

- A trap is a static piece that acts as a terminal state.  
- A wall is a "non-visitable" piece. 

- The Policy Iteration algorithm combines both the policy evaluation and policy improvement algorithms, for simplicity's sake we will make one class algorithm (policy iteration) encapsulating both policy evaluation and policy improvement.


> [!WARNING]
> //FIXME: Running into a lot of cross-references between classes

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
- [x] EpsilonGreedyPolicy(Policy) (mdp: MDP, epsilon: float, policy: dict[Piece, dict[Action, float]])
  * self.mdp: MDP
  * self.policy: dict[Piece, dict[Action, float]]
  * self.epsilon: float
  * select_action(state: Piece, q_values: dict[Piece, dict[Action, float]]) -> Action
- [x] Policy (mdp: MDP, policy: dict[Piece, dict[Action, float]] = None)
  * self.mdp: MDP
  * self.actions: list[Actions]
  * self.board: Board
  * self.policy: dict[Piece, dict[Action, float]]
  * create_default_policy(actions: list[Action], board: Board) -> dict[Piece, dict[Action, float]]
  * update_policy_action(state: Piece, action: Action, probability: float)

### algorithms/dynamic_programming
- [x] PolicyIteration(Algorithm) (mdp: MDP, theta_threshold: float, gamma: float)
  * self.mdp: MDP
  * self.policy: dict[Piece, dict[Action, float]]
  * self.board: Board
  * self.actions: list[Action]
  * self.theta_threshold: float
  * self.gamma: float
  * run() -> tuple[Policy, dict[Piece, float]]
    * policy_evaluation(policy: Policy, mdp: MDP) -> dict[Piece, float]
    * action_evaluation(state: Piece, state_values: dict[Piece, float]) -> dict[Action, float]
- [ ] ValueIteration(Algorithm) (mdp: MDP, theta_threshold: float, gamma: float)
  * self.mdp: MDP
  * self.policy: dict[Piece, dict[Action, float]]
  * self.board: Board
  * self.actions: list[Action]
  * self.theta_threshold: float
  * self.gamma: float
  * run() -> tuple[Policy, dict[Piece, float]]
    * action_evaluation(state: Piece, state_values: dict[Piece, float]) -> dict[Action, float]
  
### algorithms/monte_carlo
- [x] MonteCarloController (mdp: MDP, discount: float = 0.9, epsilon: float = 0.1, seed: int = 42, start_coords: tuple[int, int] = (0,0))
  * self.start_coords: tuple[int, int]
  * self.mdp: MDP
  * self.discount: float
  * self.epsilon: float
  * self.rng: np.RandomState
  * self.policy: EpsilonGreedyPolicy
  * self.q_values: dict[Piece, dict[Action, float]]
  * self.returns: dict[tuple[Piece, Action], list[float]]
  * update_q_values(trajectory: Trajectory)
  * train(n_episodes: int)
- [x] MonteCarloPredictor (mdp: MDP, discount: float, seed: int = 42, start_coords: tuple[int, int] = (0,0))
  * self.mdp: MDP
  * self.discount: float
  * self.returns: dict[Piece, list[]] <!--Correct this, I have no idea what to typehint here tbh-->
  * self.value_functions: dict[Piece, int] <!--Correct this, I have no idea what to typehint here tbh-->
  * self.start_coords: tuple[int, int]
  * self.rng: np.RandomState
  * evaluate_policy(policy: Policy, n_samples: int = 1_000)
  * update_value_function(trajectory: Trajectory)
  
### algorithms/temporal_difference
- [ ] QLearning(TDControl)
  * update_q_values(state: Piece, action: Action, reward: float, state_prime: Piece, _: None = None) -> None
  * run() -> dict[Piece, dict[Action, float]]
- [ ] Sarsa(TDControl)
  * update_q_values(state: Piece, action: Action, reward: float, state_prime: Piece, action_prime: Action) -> None
  * run() -> dict[Piece, dict[Action, float]]
- [ ] TDControl(ABC) (num_episodes: int, mdp: MDP, alpha: float = 0.5, epsilon: float = 0.1, gamma: float = 0.9)
  * self.num_episodes: int
  * self.mdp: MDP
  * self.alpha: float
  * self.epsilon: float
  * self.gamma: float
  * self.q_values: dict[Piece, dict[Action, float]]
  * self.policy: EpsilonGreedyPolicy
  * init_q_values() -> dict[Piece, dict[Action, float]]
  * update_q_values(state: Piece, action: Action, reward: float, state_prime: Piece, action_prime: Action|None = None) -> None
  * run() -> dict[Piece, dict[Action, float]]

### episode
- [x] Trajectory(dataclass)
  * states: list[Piece]
  * actions: list[Action]
  * rewards: list[float]
- [ ] Episode (policy: Policy, mdp: MDP, seed: int = 42, max_depth: int = 1000, start_agent_coordinates: list[int] = [0,0], live_render: bool = False)
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
  * self.pieces: list[list[Piece]]
  * observe_pieces(): dict <!--Deprecated?-->
- [x] Piece (is_terminal: bool, location: list[int], start_location: list[int], reward: float, is_visitable: bool, character: str, color: str)
  * self.is_terminal: bool
  * self.location: list[int]
  * self.start_location: list[int]
  * self.reward: float
  * self.is_visitable: bool <!--Deprecated?-->
  * self.color: str

### transition_space
- [x] TransitionMatrix (mdp: MDP, action: Action)
  * self.mdp: MDP
  * self.action: Action
  * self.matrix: dict[Piece, dict[Piece, float]]
  * build_transition_matrix(board: Board, action: Action) -> dict[Piece, dict[Piece, float]]
  * get_successor_state(state: Piece) -> dict[Piece, float]

### utils
- [x] map_loader
  * load_config(path_config: Path) -> dict
  * read_map(path_map) -> list[list[int]]
  * init_piece(piece_vals: dict[str, Any], coordinates: list[int]) -> Piece
  * load_map(path_config: Path, path_map: Path) -> list[list[Piece]]

- [x] MDP (actions: list[Action], board: Board, transition_matrices: dict[Action, TransitionMatrix] = None)
  * self.actions: list[Actions]
  * self.board: Board
  * self.transition_matrices: dict[Action, TransitionMatrix]


## Directory Tree
```
│   __init__.py
├───env_core
│   │   mdp.py
│   │   __init__.py
│   ├───action_space
│   │       action.py
│   │       __init__.py
│   ├───algorithms
│   │   │   __init__.py
│   │   ├───common
│   │   │       algorithm.py
│   │   │       epsilon_greedy_policy.py
│   │   │       policy.py
│   │   │       __init__.py
│   │   ├───dynamic_programming
│   │   │       policyiteration.py
│   │   │       valueiteration.py
│   │   │       __init__.py
│   │   ├───monte_carlo
│   │   │       first_visit_mc_control.py
│   │   │       first_visit_mc_prediction.py
│   │   │       __init__.py
│   │   │
│   │   └───temporal_difference
│   │           q_learning.py
│   │           sarsa.py
│   │           td_control.py
│   │           __init__.py
│   ├───config
│   │       action_config.json
│   │       piece_config.json
│   ├───episode
│   │       episode.py
│   │       __init__.py
│   ├───maps
│   │       danger_holes.csv
│   │       double_fish.csv
│   │       easy.csv
│   │       example.csv
│   │       wall_of_death.csv
│   ├───state_space
│   │       board.py
│   │       piece.py
│   │       __init__.py
│   ├───transition_space
│   │       transition_matrix.py
│   │       __init__.py
│   └───utils
│           map_loader.py
│           render.py
│           __init__.py
└───tests
        __init__.py
```


---
// TODO: 
Don't forget: A function that prints the state-action values for each state-action pair.
