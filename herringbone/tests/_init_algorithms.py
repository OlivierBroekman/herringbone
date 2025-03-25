from herringbone.env_core.mdp import MDP
from herringbone.env_core.episode import Episode
from herringbone.env_core.algorithms.monte_carlo.first_visit_mc_prediction import MonteCarloPredictor
from herringbone.env_core.algorithms.monte_carlo.first_visit_mc_control import MonteCarloController
from herringbone.env_core.algorithms.common.epsilon_greedy_policy import EpsilonGreedyPolicy
import sys

# init an MDP
try:
    state_path = "herringbone/env_core/config/state_config.json"
    map_path = f"herringbone/env_core/maps/easy.csv"
    action_path = "herringbone/env_core/config/action_config.json"
    demo_mdp = MDP(state_path, map_path, action_path)
except Exception as e:
    print(f"MDP initialization failed: {e}", file=sys.stderr)
    raise RuntimeError("MDP initialization failed.") from e

# Init a Policy
try:
    policy = EpsilonGreedyPolicy(mdp=demo_mdp, epsilon=1)  # defaults to uniform
except Exception as e:
    print(f"Policy initialization failed: {e}", file=sys.stderr)
    raise RuntimeError("Policy initialization failed.") from e

# Init an Episode
try:
    episode = Episode(mdp=demo_mdp, policy=policy, max_depth=3)
except Exception as e:
    print(f"Episode initialization failed: {e}", file=sys.stderr)
    raise RuntimeError("Episode initialization failed.") from e


# Init an MC predictor
try:
    N = 5
    mc_predictor = MonteCarloPredictor(demo_mdp, discount=0.9 )
    mc_predictor.evaluate_policy(policy, n_samples=N)
except Exception as e:
    print(f"MonteCarloPredictor initialization failed: {e}", file=sys.stderr)
    raise RuntimeError("MonteCarloPredictor initialization failed.") from e
 
# Init an MC Controller
try:
    mc_control = MonteCarloController(demo_mdp, discount=0.9, epsilon=0.1)
    mc_control.train(n_episodes=N)
except Exception as e:
    print(f"MonteCarloController initialization failed: {e}", file=sys.stderr)
    raise RuntimeError("MonteCarloController initialization failed.") from e


print("All initialization tests passed.")