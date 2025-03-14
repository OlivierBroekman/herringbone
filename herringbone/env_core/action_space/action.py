class Action:
    """This class represents the actions for a reinforcement learning problem."""
    def __init__(
            self, 
            config: dict
            ):
        
        self.__id = config["id"]
        self._type = config["type"]
        self._directions = config["directions"]
        self._probabilities = config["probabilities"]
        assert sum(config["probabilities"]) == 1
        assert len(config["probabilities"]) == len(config["directions"])
        self._cost = config["cost"]
        self._value = 0

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
    
    def set_directions(
            self, 
            new_directions: list[list[int]]
            ):
        
        self._directions = new_directions

    def get_directions(
            self
            ) -> list[list[int]]:
        
        return self._directions
    
    def set_probabilities(
            self, 
            new_probs: list[float]
            ):
        
        self._probabilities = new_probs

    def get_probabilities(
            self
            ) -> list[float]:
        
        return self._probabilities
    
    def set_cost(
            self, 
            new_cost: int
            ):
        
        self._cost = new_cost
    
    def get_cost(
            self
            ) -> int:
        
        return self._cost
    
    def set_value(
            self, 
            new_val: float
            ):
        
        self._value = new_val
    
    def get_value(
            self
            ) -> float:
        
        return self._value