from abc import ABC, abstractmethod

import numpy as np

from yaaf.environments.Environment import Environment
from yaaf.runners.Runner import Timestep


class MarkovDecisionProcessEnvironment(Environment, ABC):
    """
    The main interface for a Markov Decision Process

    Attributes:

    """

    def __init__(self, name, num_actions, render):

        self._states = self._generate_states()

        self._num_states = len(self._states)
        self._num_actions = num_actions

        self._P = self._generate_transition_probabilities_matrix()
        self._C = self._generate_cost_matrix()

        sample_state = self._states[0]
        observation_space = sample_state.shape

        super(MarkovDecisionProcessEnvironment, self).__init__(name, observation_space, self._num_actions, render)

    @property
    def states(self):
        return self._states

    @property
    def num_states(self):
        return self._num_states

    @property
    def num_actions(self):
        return self._num_actions

    @staticmethod
    def state_index_from(states, state):
        s = [np.array_equal(state, other_state) for other_state in states].index(True)
        return s

    def state_index(self, state):
        s = self.state_index_from(self.states, state)
        return s

    @property
    def C(self):
        return self._C

    @property
    def P(self):
        return self._P

    def value_iteration(self, discount_factor=0.99, min_error=10e-8):

        """
        Solves the MDP using value iteration
        Returns the Optimal Q function Q*
        """

        A = self.num_actions
        X = self.num_states
        P = self._P
        C = self._C

        J = np.zeros(X)
        Q = np.zeros((X, A))

        error = 1.0
        while error > min_error:
            for a in range(A):
                Q[:, a] = (C[:, a] + discount_factor * P[a].dot(J))
            Q_actions = tuple([Q[:, a] for a in range(A)])
            J_new = np.min(Q_actions, axis=0)
            error = np.linalg.norm(J_new - J)
            J = J_new

        return Q

    @abstractmethod
    def _initial_state(self):
        raise NotImplementedError()

    @abstractmethod
    def _transition(self, action):
        raise NotImplementedError()

    #########################
    # Environment Interface #
    #########################

    def _step(self, action):
        next_state, is_terminal, info = self._transition(action)
        s1 = self.state_index_from(self.states, self.state)
        cost = self._C[s1, action]
        return Timestep(self.state, action, cost * -1.0, next_state, is_terminal, info)

    def _reset(self):
        return self._initial_state()

    #############
    # Auxiliary #
    #############

    @abstractmethod
    def _generate_states(self):
        raise NotImplementedError()

    @abstractmethod
    def _generate_transition_probabilities_matrix(self):
        raise NotImplementedError()

    @abstractmethod
    def _generate_cost_matrix(self):
        raise NotImplementedError()
