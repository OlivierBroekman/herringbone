from herringbone.env_core.action_space import Action
from herringbone.env_core.state_space import Piece, Board
from herringbone.env_core.mdp import MDP
from herringbone.env_core.algorithms import Algorithm, Policy


class ValueIteration(Algorithm):
    def __init__(
            self,
            mdp: MDP,
            theta_threshold: float,
            gamma: float
    ):
        assert 0 <= theta_threshold <= 1 and 0 <= gamma <= 1
        self._mdp = mdp
        self._policy = Policy(mdp=self.get_mdp()).get_policy()
        self._board = mdp.get_board()
        self._actions = mdp.get_actions()
        self._theta_threshold = theta_threshold
        self._gamma = gamma

    # Setters and getters
    def get_mdp(
            self
    ) -> MDP:

        return self._mdp

    def set_policy(
            self, new_policy: dict[Piece, dict[Action, float]]
    ):

        self._policy = new_policy
    
    def get_policy(
            self
    ) -> dict[Piece, dict[Action, float]]:

        return self._policy
    
    def get_board(
            self
    ) -> Board:

        return self._board
    
    def get_actions(
            self
    ) -> list[Action]:

        return self._actions
    
    def get_theta_threshold(
            self
    ) -> float:

        return self._theta_threshold
    
    def get_gamma(
            self
    ) -> float:

        return self._gamma
    

    def run(
            self
    ) -> tuple[Policy, dict[Piece, float]]:
        
        def action_evaluation(
                state: Piece,
                state_values: dict[Piece, float]
        ) -> dict[Action, float]:
            """Evaluate all actions at a state"""

            actions = mdp.get_actions()

            action_values = {action: 0 for action in actions}

            for action in actions:
                for new_state, transition_probability in mdp.get_transition_matrices()[action].get_matrix()[state].items():
                    action_values[action] += (transition_probability
                                              * (state.get_reward()
                                                 + self.get_gamma()
                                                 * state_values[new_state]))
            return action_values
        
        states = self.get_mdp().get_states()
        policy = self.get_policy()
        mdp = self.get_mdp()

        state_values = {state: 0 for state in states}

        delta = 0

        # Value Iteration
        while delta <= self.get_theta_threshold():
            for state in states:
                # Find the maximum value of all actions at the current state
                action_values = action_evaluation(state=state, state_values=state_values)
                best_action_value = max(action_values.values())

                # Update stopping condition
                delta = max(delta, abs(best_action_value - state_values[state]))

                # Updat value function
                state_values[state] = best_action_value

        # Get the policy
        for state in states:
            # Get best action
            action_values = action_evaluation(state=state, state_values=state_values)
            best_action = max(action_values, key=action_values.get)

            # Greedily take the best action at the current state
            policy[state][best_action] = 1
        
        return policy, state_values

