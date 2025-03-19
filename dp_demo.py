import herringbone as hb
from demo import demo_mdp
gamma = 1.0
theta_threshold = 0.01
# seed = 42

def preview_V(mdp, learned_V):
    
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


mdp = demo_mdp
policy_iteration = hb.PolicyIteration(mdp=mdp, theta_threshold=theta_threshold, gamma=gamma)
policy, state_values = policy_iteration.run()

print(f'Succesfully created a policy!')

preview_V(mdp=mdp, learned_V=state_values)