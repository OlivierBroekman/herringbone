# %% 
"""Since git does not have propper notebook support, I recommend using cell notation."""
# %%
"""I put the psuedo code from the docs below"""

# %%
# load paths 
file_path = "maps/default.csv"
actions_config = "actions/config.json"
 
# %%
# Load in configs
states = Board(file_path)

# read out actions_config into a variable
actions = [action() for action in actions_cfg]

# %%
# Set up a policy and algorithm
policy = Policy(actions, states)

PolicyIteration(Algorithm)

algorithm = PolicyIteration(policy, threshold_theta, gamma) # INCL. OR PolicyIteration(policy)

# %%
# Train the agent
for e in episodes:   
    ep = Episode(algorithm: Algorithm, max_depth)


    if ep.run():
        reward = ep.get_reward()
        
        algorithm.update_policy(policy, reward)
        
# %% 
# animate final policy
final_ep = Episode(algorithm, max_depth)
final_ep.show = True
final_ep.run()

# %%
import herringbone

# Create a Piece instance
hw = herringbone.Piece(
    is_terminal=False,
    location=[1, 2],
    start_location=[0, 0],
    reward=10.0,
    is_visitable=True,
    character="hello_world!",
    color="red",
    value=5.0
)

print(hw)

# %%
