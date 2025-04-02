import random
from herringbone.env_core.action_space import Action
from herringbone.env_core.state_space import State, Board
from herringbone.env_core.mdp import MDP


class Policy:
    """This class represents a policy."""
    def __init__(
            self,
            mdp: MDP,
            policy: dict[State, dict[Action, float]] = None
    ):        
        self._mdp = mdp
        self._actions = mdp.get_actions()
        self._board = mdp.get_board()
        if policy != None: self._policy = policy
        else: self._policy = self.create_default_policy(actions=mdp.get_actions(), board=mdp.get_board())

    def create_default_policy(
            self, 
            actions: list[Action], 
            board: Board
    ) -> dict[State, dict[Action, float]]:
        
        """
        Creates a default, uniform policy,
        Where every action is just as likely as any other in any state.

        Args:
            actions: list[Action]: List of actions retrieved from action_config.json
            board: Board: Board retrieved from state_config.json

        Returns:
            dict[State, dict[Action, float]]: A nested dictionary mapping states and actions to probabilities
        """
        
        states = [state for row in board.states for state in row]
        m_actions = len(actions)

        policy = {state: {action: (1/m_actions) for action in actions} for state in states}
    
        return policy

    def update_policy_action(self, state: State, action: Action, probability: float, auto_normalization: bool = False):
        """Updates the probability of taking a specific action in a given state.

        Args:
            state (State): current state
            action (Action): chosen action
            probability (float): new probability
            auto_normalization (bool, optional): whether the transition probabilities should be normalized. Defaults to False.

        Raises:
            ValueError: invalid state
            ValueError: invalid action
            ValueError: sum of all probabilities cannot be zero
        """
        if state not in self._policy:
            raise ValueError("State not found in policy.")
        
        if action not in self._policy[state]:
            raise ValueError("Action not found in policy.")

        # Update the action probability
        self._policy[state][action] = probability

        # Normalize
        total_prob = sum(self._policy[state].values())
        
        if total_prob == 0:
            raise ValueError("Total probability for state is zero, cannot normalize.")
    
        for a in self._policy[state]:
            self._policy[state][a] /= total_prob
            
    def hard_max(self):
        for state, actions in self._policy.items():
            if not state._is_terminal:
                max_action = max(actions, key=actions.get)
                for action in actions:
                        actions[action] = 1.0 if action == max_action else 0.0

    
    def get_next_action(
        self,
        state: State,
        q_values: dict[State, dict[Action, float]]
    ) -> Action:
        """Return the best possible action at  the current state

        Args:
            state (State): current state
            q_values (dict[State, dict[Action, float]]): state-action values look-up table

        Returns:
            Action: the best possible action
        """
        
        actions = list(q_values[state].keys()) 
        probabilities = list(q_values[state].values())  

        return random.choices(actions, weights=probabilities, k=1)[0]
        
    def __str__(self): 

        
        best_actions = [[
            [a for a, v in self._policy[state].items() if v == max(self._policy[state].values())]
            for state in row
        ] for row in self._board.states]

        len_char = max(
            len("/".join(a.get_character() for a in actions)) if actions else 0
            for row in best_actions for actions in row
        )
        num_cols = len(best_actions[0]) if best_actions else 0

        grid = f"╔{('═' * (len_char + 2) + '╦') * (num_cols - 1)}{'═' * (len_char + 1)}═╗\n"

        for i_row, row in enumerate(best_actions):
            grid += f"║ {" ║ ".join(
                f"{'/'.join(a.get_character() for a in actions).center(len_char)}" if actions else " "
                for actions in row
            )} ║\n"

            if i_row < len(best_actions) - 1:
                grid += "╠" + ('═' * (len_char + 2) + '╬') * (num_cols - 1) + '═' * (len_char + 1) + "═╣\n"

        grid += f"╚{('═' * (len_char + 2) + '╩') * (num_cols - 1) + '═' * (len_char + 1)}═╝"
        return grid

    
    # Setters and getters
    def get_mdp(
            self
    ) -> MDP:
        
        return self._mdp

    def get_actions(
            self
    ) -> list[Action]:
        
        return self._actions

    def get_board(
            self
    ) -> Board:
        
        return self._board

    def set_policy(
            self,
            new_policy: dict[State, dict[Action, float]]
    ):
        
        self._policy = new_policy

    def get_policy(
            self
    ) -> dict[State, dict[Action, float]]:
        
        return self._policy
