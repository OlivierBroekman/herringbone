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
        self._character = config["char"]

    def get_id(self):
        return self.__id

    def __str__(self):
        return f"{self._character}"
    
    def __repr__(self):
        return f"{self._character}"
   
    # Getters
    def get_type(
            self
    ) -> str:
        
        return self._type

    def get_directions(
            self
    ) -> list[list[int]]:
        
        return self._directions

    def get_probabilities(
            self
    ) -> list[float]:
        
        return self._probabilities
    
    def get_cost(
            self
    ) -> int:
        
        return self._cost

    def get_character(
            self
    ) -> str:
        
        return self._character