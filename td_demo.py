from herringbone import MDP, QLearning, Sarsa


mdp = MDP(
    "herringbone/env_core/config/state_config.json",
    "herringbone/env_core/maps/example.csv",
    "herringbone/env_core/config/action_config.json",
)


model = QLearning(num_episodes=100, mdp=mdp)
model.run()

for state, vals in model.q_values.items():
    print(f"{state.get_location()} has Q-values {vals}")
