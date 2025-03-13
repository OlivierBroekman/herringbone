import herringbone as hb
from demo import demo_mdp
discount = 0.9
epsilon = 0.1
seed = 42

# Prediction
mdp = demo_mdp
policy = hb.EpsilonGreedyPolicy(mdp=demo_mdp, epsilon=1)  # defaults to uniform
mc_predictor = hb.MonteCarloPredictor(mdp, discount=discount, seed=seed)
mc_predictor.evaluate_policy(policy, n_samples=100)
learned_V = mc_predictor.value_functions


# This is all needed just to print a value function? sure we don't want to make this a class? or am i just stewpid. 
# Maybe a util is better? display_value_function(value_func)
states_2d = mdp.get_board().pieces
x = len(states_2d)
y = len(states_2d[0])

for s,v in learned_V.items():
    print(f"state: {s} | value: {v}")

v_values =  ['%.2f' % v for v in list(learned_V.values())]

two_d_list = [v_values[i * y:(i + 1) * y] for i in range(x)]

# Print 2D list
for row in two_d_list:
    print(row)
    
    
# # Control
# mc_control = MonteCarloPredictor(mdp, discount=discount, epsilon=epsilon, seed=seed)
# mc_control.train(n_episodes=1000)
# optimal_policy = mc_control.policy
