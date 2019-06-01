from collections import defaultdict

import numpy as np

from yaaf.agents.TrainableAgent import TrainableAgent
from yaaf.policies.EpsilonGreedyPolicy import EpsilonGreedyPolicy


class SARSAAgent(TrainableAgent):

    def __init__(self, action_space, name="SARSA", train=True, load_from=None,
                 learning_rate=0.3, discount_factor=0.99, exploration_rate=0.05):
        self._Q = defaultdict(lambda: np.zeros(action_space))
        self._learning_rate = learning_rate
        self._discount_factor = discount_factor
        evaluation_policy = EpsilonGreedyPolicy(action_space, 0.0)
        training_policy = EpsilonGreedyPolicy(action_space, exploration_rate)
        super(SARSAAgent, self).__init__(name, evaluation_policy, training_policy, train, load_from)

    @property
    def Q(self):
        return self._Q

    ###################
    # Agent Interface #
    ###################

    def policy(self, state):
        distribution = self._policy.distribution(state, q_values=self._Q[tuple(state)])
        return distribution

    #############################
    # Trainable Agent Interface #
    #############################

    def _reinforce(self, timestep):
        s1 = tuple(timestep.state)
        a = timestep.action
        s2 = tuple(timestep.next_state)

        alpha = self._learning_rate
        gamma = self._discount_factor

        Q_s1_a = self._Q[s1][a]
        Q_s2_a = self._Q[s2][a]

        r = timestep.reward

        self._Q[s1][a] = Q_s1_a + alpha * (r + gamma * Q_s2_a - Q_s1_a)

    def _save(self, directory):
        # TODO
        pass

    def load(self, directory):
        # TODO
        pass
