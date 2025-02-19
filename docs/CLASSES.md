### Terminology  
- piece: an object on the board (e.g., agent, predator, wall).  
- board: a 2D array of pieces.
- reward: positive values indicate a reward, while negative values indicate a cost. Rewards are cumulative.  

> Note: "Colliding" with a piece grants a reward; collisions are piece-based, not cell-based. This allows for dynamic objects.  
> A trap is a static piece that acts as a terminal state.  
> A wall is a "non-visitable" piece. 

> The Policy Iteration algorithm combines both the policy evaluation and policy improvement algorithms, for simplicity's sake we will make one class algorithm (policy iteration) encapsulating both policy evaluation and policy improvement.

//FIXME: Running into a lot of cross-references between classes

### State Space  
- [ ] boardfile
  * piece[][]: self.pieces = map_loader.load_map(filepath)  
  * observe_pieces() -> dict(piece, [x,y])  
  * \__str__()

- [x] piece class  
  * config.json  
  * self.is_terminal  
  * self.location  
  * self.start_location
  * self.reward #TODO help  
  * self.is_visitable
  * self.character
  * self.color

### Action Space  
- [x] action class  
  * config.json  
  * self.type  
  * self._id  
  * self.cost (negative!)  
  * self.movement  

### Main Policy  
//TODO: Improve upon the episode class
- [ ] episode (algorithm, policy, max_depth)
  * self.algorithm
  * self.policy
  * self.max_depth
  * get_reward(policy) -> float
  * update_policy()
<!-- - [ ] episode (actions, states, policy)
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
      * get_action_reward()   -->

- [x] policy (float[][] = None)
  * self.policy (can be passed an existing policy, if no policy is passed assume default policy)
  * create_policy(states, actions) -> policy 

- [x] algorithm (policy) (abstract class)
  * self.policy
  * run() -> policy

- [ ] policyiteration (policy, theta_threshold, gamma) (algorithm subclass) 
  * self.policy
  * self.theta_threshold
  * self.gamma
  * run() -> policy

- [ ] valueiteration(states, actions, theta_threshold, gamma)
  * self.states
  * self.actions
  * self.theta_threshold
  * self.gamma
  * run() -> float[][]
  * find_policy(float[][]) -> policy

### Utils  
- [x] map_loader




---
// TODO: 
Don't forget: A function that prints the state-action values for each state-action pair.
