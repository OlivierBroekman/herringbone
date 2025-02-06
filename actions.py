import numpy as np
import json

class Action:
    def __init__(self, config: str):
        with open(config, 'r') as file:
            self.actions = json.load(file)
    
    def get_cost(self, action: str):
        if action not in self.actions.keys():
            return -1
        else:
            return self.actions[action]["cost"]
        
    def set_cost(self, action: str, new_cost: int):
        if action not in self.actions.keys():
            return -1
        else:
            self.actions[action]["cost"] = new_cost