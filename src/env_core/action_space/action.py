class Action:
    """This class represents the actions for a reinforcement learning problem."""
    def __init__(
            self, 
            config: dict
            ):
        
        self.__id = config["id"]
        self._type = config["type"]
        self._direction = config["direction"]
        self._cost = config["cost"]

    # Setters and getters
    def set_type(
            self, 
            new_type: str
            ): 
        
        self._type = new_type
    
    def get_type(
            self
            ) -> str:
        
        return self._type
    
    def set_direction(
            self, 
            new_direction: list[int]
            ):
        
        self._direction = new_direction

    def get_direction(
            self
            ) -> list[int]:
        
        return self._direction
    
    def set_cost(
            self, 
            new_cost: int
            ):
        
        self._cost = new_cost
    
    def get_cost(
            self
            ) -> int:
        
        return self._cost