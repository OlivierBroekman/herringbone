#TODO BURN AFTER READING

import herringbone as hb
import json

# quick config

map_names = ["example", "easy", "danger_holes", "double_fish", "wall_of_death"]


state_path = "herringbone/env_core/config/state_config.json"
map_path = f"herringbone/env_core/maps/{map_names[1]}.csv"
action_path = "herringbone/env_core/config/action_config.json"

demo_mdp = hb.MDP(state_path, map_path, action_path, seed=10)


random_policy = hb.EpsilonGreedyPolicy(mdp=demo_mdp, epsilon=1)
episode = hb.Episode(mdp=demo_mdp, policy=random_policy, max_depth=1000)

# render single frames for all render modes
print("Render modes:")
hb.Render.preview_frame(demo_mdp.get_board(),demo_mdp.get_states()[2],"rewards")
hb.Render.preview_frame(demo_mdp.get_board(),demo_mdp.get_states()[2],"ascii")
hb.Render.preview_frame(demo_mdp.get_board(),demo_mdp.get_states()[2],"sar")

# Shows peek (the board)
print("Board peek:")
episode.peek(render_mode="rewards")\

# Runs with live trajectory
print("Live episode:")
episode.run("sar")

# Animate a ran episode
print("Final animation:")
hb.Render.animate(demo_mdp, episode.trajectory, "ascii",pause=0.5)


