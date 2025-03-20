import herringbone as hb


# create an MDP
map_names = ["example", "easy", "danger_holes", "double_fish", "wall_of_death"]
selected_map_id = 0

state_path = "herringbone/env_core/config/state_config.json"
map_path = f"herringbone/env_core/maps/{map_names[1]}.csv"
action_path = "herringbone/env_core/config/action_config.json"

demo_mdp = hb.MDP(state_path, map_path, action_path, seed=42)


random_policy = hb.EpsilonGreedyPolicy(mdp=demo_mdp, epsilon=1)
episode = hb.Episode(mdp=demo_mdp, policy=random_policy, max_depth=1000)

episode.run("sar")
