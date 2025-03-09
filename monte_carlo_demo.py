### main
from herringbone import MDP, MonteCarloPredictor, MonteCarloPredictor, Policy

discount = 0.9
epsilon = 0.1
seed = 42

# Prediction
mdp = MDP()
policy = Policy(mdp)  # defaults to uniform
mc_predictor = MonteCarloPredictor(mdp, discount=discount, seed=seed)
mc_predictor.evaluate_policy(policy, n_samples=1000)

# Control
mc_control = MonteCarloPredictor(mdp, discount=discount, epsilon=epsilon, seed=seed)
mc_control.train(n_episodes=1000)
optimal_policy = mc_control.policy
