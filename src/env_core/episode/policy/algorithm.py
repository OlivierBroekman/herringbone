from policy import Policy
from abc import ABC, abstractmethod

class Algorithm(ABC):
    def __init__(self, policy: Policy):
        self._policy = policy
    
    # Setter and getter
    @property
    def policy(self) -> Policy:
        return self._policy
    
    @policy.setter
    def policy(self, new_policy: Policy):
        self._policy = new_policy


    @abstractmethod
    def run(self) -> Policy:
        pass