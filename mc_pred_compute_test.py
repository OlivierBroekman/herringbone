import time
import numpy as np
import matplotlib.pyplot as plt
import herringbone as hb  # Assuming hb is the library you're using


# create an MDP
map_names = ["slides", "example", "easy", "danger_holes", "double_fish", "wall_of_death", "example2", "mega"]
selected_map_id = 0

state_path = "herringbone/env_core/config/state_config.json"
map_path = f"herringbone/env_core/maps/{map_names[selected_map_id]}.csv"
action_path = "herringbone/env_core/config/action_config.json"

demo_mdp = hb.MDP(state_path, map_path, action_path, seed=42, gamma=1)

step_size = 1000
# Define parametersxw
N_values = [i * step_size for i in range(1, 11)]  # Different N values to test
execution_times = []

# Initialize Monte Carlo predictor

policy = hb.Policy(mdp=demo_mdp)
mc_predictor = hb.MonteCarloPredictor(demo_mdp)

# Measure execution time for each N
for N in N_values:
    start_time = time.time()
    mc_predictor.evaluate_policy(policy, n_samples=N)
    end_time = time.time()
    
    execution_time = end_time - start_time
    execution_times.append(execution_time)
    print(f"N = {N}, Time = {execution_time:.4f} seconds - {execution_time/N}")

# Compute the ratios
ratios = [execution_times[i] / N_values[i] for i in range(len(N_values))]

# Compute the average of these ratios
average_ratio = sum(ratios) / len(ratios)

print("Average Ratio:", average_ratio)
print(execution_times)

hb.Render.preview_V(learned_V=mc_predictor.value_functions, mdp=demo_mdp)