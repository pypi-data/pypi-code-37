from yaaf.agents.TrainableAgent import TrainableAgent
from yaaf.models.DeepQNetwork import DeepQNetwork
from yaaf.policies.EpsilonGreedyPolicy import EpsilonGreedyPolicy


class DeepQNetworkAgent(TrainableAgent):

    def __init__(self, action_space, name="DeepQNetwork", train=True, load_from=None,
                 screen_width=84, screen_height=84, stacked_frames=4,
                 convolutional_layers=((8, 16, 4, "relu"), (4, 32, 2, "relu")), fully_connected_layers=((256, "relu"),),
                 start_exploration_rate=0.75, end_exploration_rate=0.05, exploration_rate_decay=0.05,
                 learning_rate=0.001, loss="mse", dropout_rate=0.0,
                 discount_factor=0.99, replay_memory_size=1000000, replay_memory_batch=32):
        self._learning_rate = learning_rate
        self._discount_factor = discount_factor

        self._exploration_rate = start_exploration_rate
        self._min_exploration_rate = end_exploration_rate
        self._exploration_rate_decay = exploration_rate_decay

        self._deep_q_network = DeepQNetwork(screen_width, screen_height, stacked_frames, action_space,
                                            convolutional_layers=convolutional_layers,
                                            fully_connected_layers=fully_connected_layers,
                                            learning_rate=learning_rate, loss=loss, dropout_rate=dropout_rate,
                                            discount_factor=discount_factor, replay_memory_size=replay_memory_size,
                                            replay_memory_batch=replay_memory_batch)

        evaluation_policy = EpsilonGreedyPolicy(action_space, 0.0)
        training_policy = EpsilonGreedyPolicy(action_space, end_exploration_rate)

        super(DeepQNetworkAgent, self).__init__(name, evaluation_policy, training_policy, train, load_from)

    ###################
    # Agent Interface #
    ###################

    def policy(self, state):
        q_values = self._deep_q_network.predict(state)
        distribution = self._policy.distribution(state, q_values=q_values, epsilon=self._exploration_rate)
        return distribution

    #############################
    # Trainable Agent Interface #
    #############################

    def _reinforce(self, timestep):
        self._deep_q_network.train(timestep)

        if self._exploration_rate > self._min_exploration_rate:
            self._exploration_rate *= self._exploration_rate_decay

    def _save(self, directory):
        self._deep_q_network.save(directory)

    def load(self, directory):
        self._deep_q_network.load(directory)
