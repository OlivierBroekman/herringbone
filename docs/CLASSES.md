### Terminology
**piece:** an object on the board(e.g., agent, predator, wall).
**cell:** place on the board, might host a piece.
**reward:** positive is a reward, negative a cost, cumulative.

_Note that "colliding" with a piece gives a reward, not colliding with a specific cell! This to make movable objects possible.
 A trap (terminal state) is just a static piece, a wall is a "non-visitable" piece._


### State Space

- board
-- self.map_loader
-- render()
-- self.cells == cell[ ][ ]
-- observe_pieces() -> dict(piece, [x,y])

- cell class
-- self.coordinates
-- self.piece

- piece class
-- config.json
-- self.terminal
-- self.location
-- self.start_location
-- self.collision_reward #TODO help
-- self.is_visitable
-- self.reset()
-- step(curr_state, action) -> new_state, reward

### Action Space
- action class
-- config.json
-- self.type
-- self._id
-- self.reward (negative!)
-- self.movement

### Main Policy
- episode
-- self.total_reward
-- get_step_count()
-- self.history (<s,a,r>)
-- self.action_space = load_actions()
-- self.state_space()
-- self.policy
-- run_episode()
-- sample_action() = self.policy.get_next(self.action_space, self.state_space.sget_obs)
-- update_piece_locations()
-- calculate_new_reward(last_action, new_location)
--- get_location_reward()
--- get_action_reward()



- policy
-- get_next() -> action_id

---
# utils
- render
config.json
-- ASCII
-- array
- map_loader
-- config.json

---
// TODO: 
Don't forget: A function that prints the state-action values for each state-action pair.
