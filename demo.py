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

demo_mdp = hb.MDP(state_path, map_path, action_path)
