from abc import ABC, abstractmethod

import numpy as np


class Policy(ABC):

    def __init__(self, name, action_space):
        self._name = name
        self._action_space = action_space

    @property
    def action_space(self):
        return self._action_space

    @abstractmethod
    def distribution(self, state, **kargs):
        raise NotImplementedError()

    def action(self, state, **kargs):
        distribution = self.distribution(state, **kargs)
        action = np.random.choice(range(self._action_space), p=distribution)
        return action
