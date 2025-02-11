### Terminology  
- piece: an object on the board (e.g., agent, predator, wall).  
- board: a 2D array of pieces.
- reward: positive values indicate a reward, while negative values indicate a cost. Rewards are cumulative.  

> Note: "Colliding" with a piece grants a reward; collisions are piece-based, not cell-based. This allows for dynamic objects.  
> A trap is a static piece that acts as a terminal state.  
> A wall is a "non-visitable" piece.  

### State Space  
- [ ] boardfile
  * piece[][]: self.pieces = map_loader.load_map(filepath)  
  * observe_pieces() -> dict(piece, [x,y])  

- [x] piece class  
  * config.json  
  * self.terminal  
  * self.location  
  * self.collision_reward #TODO help  
  * self.is_visitable  

### Action Space  
- [x] action class  
  * config.json  
  * self.type  
  * self._id  
  * self.reward (negative!)  
  * self.movement  

### Main Policy  
//TODO: NEED TO BE DISCUSSED ASAP.
- [ ] episode (actions, states, policy)
  * self.action_space
  * self.state_space  
  * self.total_reward  
  * get_step_count()  
  * boards[][] = self.history
  * self.policy  
  * run()
  * update_policy()
  * PREV:
    * sample_action() = self.policy.get_next(self.action_space, self.state_space.get_obs)  
    * update_piece_locations()  
    * calculate_new_reward(last_action, new_location)  
      * get_location_reward()  
      * get_action_reward()  

- [ ] policy  
  * get_next() -> action_id  

### utils  
- map_loader




---
// TODO: 
Don't forget: A function that prints the state-action values for each state-action pair.
