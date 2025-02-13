file_path = "maps/default.csv"
actions_config = "actions/config.json"


states = Board(file_path)

# read out actions_config into a variable
actions = [action() for action in actions_cfg]

policy = Policy(actions, states)

PolicyIteration(Algorithm)

algorithm = PolicyIteration(policy, threshold_theta, gamma) # INCL. OR PolicyIteration(policy)

for e in episodes:   
    ep = Episode(algorithm: Algorithm, max_depth)


    if ep.run():
        reward = ep.get_reward()
        
        algorithm.update_policy(policy, reward)

    # # begin extras
    # ep.render(True)
    # rew = ep.get_reward() 
    # hist = ep.get_history() # -> array_van_boards
    # print(hist)
    # # begin extras
     
    
""""
What should a policy return? -> chosen step
What should a policy look like? -> table
"""

# field,    action1,    action2,
# 0,0.      0.70,       0.30,


# episode
policy = None

# read out csv -> define (length = n) of state space
# read out actions_config -> define (length = m) of action space
# define default policy in n rows, m columns table
#   default policy: set every action to be equally likely
#   run policy in an episode and iteratively update the policy
#   after k steps of non-terminal: discard updated policy

# What is a policy???

# Parking space cursor: |  |  |  |  |