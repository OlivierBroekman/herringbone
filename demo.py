import herringbone as hb
import json

# quick config

map_names = ["example", "easy", "danger_holes", "double_fish", "wall_of_death"]

#TODO 
# I DONT LIKE  THIS? TO WHAT EXTEND ARE THESE JUST FIXED AS DEFAULTS? OTHERWISE WE CAN JUST MAKE THEM PYTHON DATA
# E.g.  hb.config_defaults.map_config?
# And when a "user" wants a custom config they can still add a path? but it seems weird to have these files in the package here.
state_path = "herringbone/env_core/config/state_config.json"
map_path = f"herringbone/env_core/maps/{map_names[0]}.csv"
action_path = "herringbone/env_core/config/action_config.json"

# board = hb.Board(path_config=state_path, path_map=map_path)

# # read out actions_config into a variable
# with open(action_path, "r", encoding='utf-8') as file: #TODO does action not have a build in reader?
#     actions_config = json.load(file)
    
# actions = [hb.Action(config) for config in actions_config.values()]


# demo_mdp = hb.MDP(actions=actions, board=board)
# print( hb.EpsilonGreedyPolicy(mdp=demo_mdp, epsilon=1))
# random_policy = hb.EpsilonGreedyPolicy(mdp=demo_mdp, epsilon=1)
# episode = hb.Episode(mdp=demo_mdp, policy=random_policy, max_depth=1000)
# episode.peek()

# episode.run()

demo_mdp = hb.MDP(state_path, map_path, action_path)
