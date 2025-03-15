from herringbone.env_core.action_space import Action
from herringbone.env_core.state_space import Piece, Board
from herringbone.env_core.mdp import MDP


class Policy:
    """This class represents a policy."""
    def __init__(
            self, 
            mdp: MDP, 
            policy: dict[Piece, dict[Action, float]] = None
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
            ) -> dict[Piece, dict[Action, float]]:
        
        """
        Creates a default, uniform policy,
        Where every action is just as likely as any other in any state.

        Arguments:
            actions: list[Action]: List of actions retrieved from action_config.json
            board: Board: Board retrieved from piece_config.json

        Returns:
            dict[Piece, dict[Action, float]]: A nested dictionary mapping states and actions to probabilities
        """
        
        states = [state for row in board.pieces for state in row]
        m_actions = len(actions)

        policy = {state: {action: (1/m_actions) for action in actions} for state in states}
    
        return policy

    def update_policy_action(self, state: Piece, action: Action, probability: float):
        """
        Updates the probability of taking a specific action in a given state.
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
  
    def __str__(self): 
        best_actions = [[max(self._policy[state], key=self._policy[state].get) for state in row]for row in self._board.pieces]
    
    
        
        len_char = max(len(a.get_character() or '') for row in best_actions for a in row)  # TODO !!!
        num_cols = len(best_actions[0]) if best_actions else 0

        grid = f"╔{('═' * (len_char + 2) + '╦') * (num_cols - 1)}{'═' * (len_char + 1)}═╗\n"

        for i_row, row in enumerate(best_actions):
            grid += f"║ {" ║ ".join(
                f"{a.get_character()}"
                for a in row)} ║\n"

            if i_row < len(best_actions) - 1:
                grid += "╠" + ('═' * (len_char + 2) + '╬') * (num_cols - 1) + '═' * (len_char + 1) + "═╣\n"

        grid += f"╚{('═' * (len_char + 2) + '╩') * (num_cols - 1) + '═' * (len_char + 1)}═╝"
        return grid


    
    # Setters and getters
    def set_mdp(
            self, 
            new_mdp: MDP
            ):
        
        self._mdp = new_mdp

    def get_mdp(
            self
            ) -> MDP:
        
        return self._mdp

    def set_actions(
            self, 
            new_actions: list[Action]
            ):
        
        self._actions = new_actions

    def get_actions(
            self
            ) -> list[Action]:
        
        return self._actions

    def set_board(
            self, 
            new_board: Board
            ): 
        
        self._board = new_board

    def get_board(
            self
            ) -> Board:
        
        return self._board

    def set_policy(
            self, 
            new_policy: dict[Piece, dict[Action, float]]
            ):
        
        self._policy = new_policy

    def get_policy(
            self
            ) -> dict[Piece, dict[Action, float]]:
        
        return self._policy
