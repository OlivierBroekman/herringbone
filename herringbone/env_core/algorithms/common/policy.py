from herringbone import MDP, Piece, Board, Action


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
        
        states = [state for row in board for state in row]
        m_actions = len(actions)

        policy = {state: {action: (1/m_actions) for action in actions} for state in states}

        return policy
    
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