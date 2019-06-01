import random

import numpy as np

from yaaf.environments.mdps.MarkovDecisionProcessEnvironment import MarkovDecisionProcessEnvironment
from yaaf.policies.Policy import Policy


class EpsilonGreedyPolicy(Policy):

    def __init__(self, action_space, epsilon, Q=None, states=None):
        super(EpsilonGreedyPolicy, self).__init__("Epsilon Greedy", action_space)
        self._epsilon = epsilon
        if Q is not None:
            assert states is not None, "Q Matrix requires additional argument (list of states) for indexing"
            self._states = states
            self._Q = Q

    def distribution(self, state, **kargs):

        if hasattr(self, "_Q"):
            s = MarkovDecisionProcessEnvironment.state_index_from(self._states, state)
            q_values = self._Q[s]
        else:
            assert "q_values" in kargs
            q_values = kargs["q_values"]

        epsilon = kargs["epsilon"] if "epsilon" in kargs else self._epsilon

        roll = random.uniform(0, 1)
        if roll < epsilon:
            distribution = np.zeros((self._action_space,)) + 1 / self._action_space
        else:
            greedy_actions = np.argwhere(q_values == np.max(q_values)).reshape(-1)
            distribution = np.zeros((self._action_space,))
            prob = 1.0 / len(greedy_actions)
            np.put(distribution, greedy_actions, prob)

        return distribution
