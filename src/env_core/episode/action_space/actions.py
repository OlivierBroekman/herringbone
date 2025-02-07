import numpy as np

class Action:
    """This class represents the actions for a reinforcement learning problem."""
    def __init__(self, config: dict):
        self.__id = config["id"]
        self._type = config["type"]
        self._direction = config["direction"]
        self._cost = config["cost"]

    # Setters and getters
    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, new_type: str):
        self._type = new_type

    @property
    def direction(self) -> list[int]:
        return self.direction

    @direction.setter
    def direction(self, new_direction: list[int]):
        self._direction = new_direction

    @property
    def cost(self) -> int:
        return self.cost

    @cost.setter
    def cost(self, new_cost: int):
        self._cost = new_cost
