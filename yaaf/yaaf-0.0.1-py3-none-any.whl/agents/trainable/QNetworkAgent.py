from yaaf.agents.TrainableAgent import TrainableAgent
from yaaf.models.QNetwork import QNetwork
from yaaf.policies.EpsilonGreedyPolicy import EpsilonGreedyPolicy


class QNetworkAgent(TrainableAgent):

    """
    A class representing a QNetwork Agent
    http://ml.informatik.uni-freiburg.de/former/_media/publications/rieecml05.pdf
    """

    def __init__(self, observation_space, action_space, name="QNetwork", train=True, load_from=None,
                 layers=((64, "relu"),),
                 learning_rate=0.001, discount_factor=0.99, loss="mse", dropout_rate=0.0,
                 initial_exploration_rate=0.75, end_exploration_rate=0.05, exploration_rate_decay=0.05,
                 replay_memory_size=1000000, replay_memory_batch=32):

        """

        Constructor:
            Returns an instance of a QNetwork Agent, setup for a given environment.

        :param observation_space:
            The environment's observation space (Tensor Shape).
            E.g. (4,).
            QNetwork Agent only supports environments where states correspond to features arrays.
            Required observation space: (F,) where F is the number of features.

        :param action_space:
            The environment's action space (int).
            E.g. 7.

        :param name:
            The name for the agent.
            Default: QNetwork.

        :param train:
            Flag for initializing the agent in training mode (learns by interacting with the environment).
            Default: True.

        :param load_from:
            Directory with pre-trained agent instance.
            Default: None.

        :param layers:
            A collection of fully connected layers as tuples like (hidden_units, activation_function).
            Default: ((64, "relu"),).

        :param learning_rate:
            The learning rate for the Adam backpropagation algorithm.
            Default: 0.001.

        :param discount_factor:
            The discount factor for reward accumulation.
            Default: 0.99

        :param loss:
            The loss for the Adam backpropagation algorithm.
            Default: mse (Mean Squared Error).

        :param dropout_rate:
            The dropout rate for the hidden layers.
            Default: 0.0 (No dropout).

        :param initial_exploration_rate:
            The initial exploration rate for the EpsGreedy Policy.
            Default: 0.75

        :param end_exploration_rate:
            The end exploration rate for the EpsGreedy Policy.
            Default: 0.05.

        :param exploration_rate_decay:
            The exploration rate's step decay.
            Default: 0.05.

        :param replay_memory_size:
            The maximum size for the agent's replay memory.
            Default: 1000000.

        :param replay_memory_batch:
            The replay memory's batch size for training.
            Default: 32.

        """

        assert len(observation_space) == 1, \
            "QNetwork Agent only supports environments where states correspond to features arrays." \
            "\nRequired observation space: (F,) where F is the number of features."

        self._features = observation_space[0]

        self._exploration_rate = initial_exploration_rate
        self._exploration_rate_decay = exploration_rate_decay
        self._min_exploration_rate = end_exploration_rate

        self._q_network = QNetwork(self._features, action_space, layers=layers,
                                   learning_rate=learning_rate, loss=loss, dropout_rate=dropout_rate,
                                   discount_factor=discount_factor, replay_memory_size=replay_memory_size,
                                   replay_memory_batch=replay_memory_batch)

        evaluation_policy = EpsilonGreedyPolicy(action_space, 0.0)
        training_policy = EpsilonGreedyPolicy(action_space, end_exploration_rate)

        super(QNetworkAgent, self).__init__(name, evaluation_policy, training_policy, train, load_from)

    ###################
    # Agent Interface #
    ###################

    def policy(self, state):
        q_values = self._q_network.predict(state)
        distribution = self._policy.distribution(state, q_values=q_values, epsilon=self._exploration_rate)
        return distribution

    #############################
    # Trainable Agent Interface #
    #############################

    def _reinforce(self, timestep):
        self._q_network.train(timestep)
        if self._exploration_rate > self._min_exploration_rate:
            self._exploration_rate *= self._exploration_rate_decay

    def _save(self, directory):
        self._q_network.save(directory)

    def load(self, directory):
        self._q_network.load(directory)
