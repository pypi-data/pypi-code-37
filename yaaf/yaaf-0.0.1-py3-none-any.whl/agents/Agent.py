from abc import ABC

import numpy as np


class Agent(ABC):

    def __init__(self, name, policy):
        self._name = name
        self._policy = policy

    @property
    def name(self):
        return self._name

    def action(self, state):
        policy = self.policy(state)
        action = np.random.choice(range(self._policy.action_space), p=policy)
        return action

    def policy(self, state):
        distribution = self._policy.distribution(state)
        return distribution
