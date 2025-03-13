from herringbone.env_core.algorithms.common import Policy
from abc import ABC, abstractmethod

class Algorithm(ABC):
    def __init__(
            self, 
            policy: Policy
            ):
        
        self._policy = policy
    
    # Setter and getter
    def set_policy(
            self, 
            new_policy: Policy
            ):
        
        self._policy = new_policy
    
    def get_policy(
            self
            ) -> Policy:
        
        return self._policy


    @abstractmethod
    def run(
        self
        ) -> Policy:
        
        pass