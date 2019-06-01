import numpy as np

from yaaf.policies.Policy import Policy


class RandomPolicy(Policy):

    def __init__(self, action_space):
        super().__init__("Random", action_space)

    def distribution(self, state, **kargs):
        return np.zeros((self._action_space,)) + 1 / self._action_space
