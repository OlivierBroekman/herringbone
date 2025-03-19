import herringbone as hb
from demo import demo_mdp
discount = 0.9
epsilon = 0.1
seed = 42


# This is all needed just to print a value function? sure we don't want to make this a class? or am i just stewpid. 
# Maybe a util is better? display_value_function(value_func)

def preview_V(mdp, learned_V):
    
    states_2d = mdp.get_board().states
    x = len(states_2d)
    y = len(states_2d[0])

    # for s,v in learned_V.items():
    #     print(f"state: {s} | value: {v}")

    v_values =  ['%.2f' % v for v in list(learned_V.values())]

    two_d_list = [v_values[i * y:(i + 1) * y] for i in range(x)]

    # Print 2D list
    for row in two_d_list:
        print(row)

# Prediction Demo
mdp = demo_mdp
# policy = hb.EpsilonGreedyPolicy(mdp=demo_mdp, epsilon=1)  # defaults to uniform
# mc_predictor = hb.MonteCarloPredictor(mdp, discount=discount, seed=seed)
# mc_predictor.evaluate_policy(policy, n_samples=10000)
# learned_V = mc_predictor.value_functions
# preview_V(mdp, learned_V)


# Control Demo
mc_control = hb.MonteCarloController(mdp, discount=discount, epsilon=0.1, seed=seed, start_coords=(0,0))
mc_control.train(n_episodes=1000)
trained_policy = mc_control.policy

print("policy trained!, now evaluating...")

print(trained_policy.get_policy())
print(trained_policy)

mc_predictor = hb.MonteCarloPredictor(mdp, discount=discount, seed=seed, start_coords=(0,0))
mc_predictor.evaluate_policy(trained_policy, n_samples=10000)
learned_V = mc_predictor.value_functions

preview_V(mdp, learned_V)

