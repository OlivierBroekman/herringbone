import numpy as np
import json

class Action:
    def __init__(self, config: dict):
        self.__id = config["id"]
        self.type = config["type"]
        self.direction = config["direction"]
        self.cost = config["cost"]

    def set_type(self, new_type: str):
        self.type = new_type
    
    def set_direction(self, new_direction: list[int]):
        self.direction = new_direction
    
    def set_cost(self, new_cost: int):
        self.cost = new_cost

    def get_type(self) -> str:
        return self.type
    
    def get_direction(self) -> list[int]:
        return self.direction
    
    def get_cost(self) -> int:
        return self.cost