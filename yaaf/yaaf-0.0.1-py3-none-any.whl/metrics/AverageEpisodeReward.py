from yaaf.metrics.Metric import Metric


class AverageEpisodeReward(Metric):

    def __init__(self, verbose=False, log_interval=5):

        super(AverageEpisodeReward, self).__init__("Average Episode Reward")

        self._verbose = verbose
        self._log_interval = log_interval

        self._episodes = 0
        self._cumulative_reward = 0.0
        self._episode_reward = 0.0
        self._average_episode_reward = 0.0

    @property
    def name(self):
        return self._name

    def __call__(self, timestep):

        is_terminal = timestep.is_terminal
        reward = timestep.reward

        self._episode_reward += reward

        if is_terminal:

            self._episodes += 1
            self._cumulative_reward += self._episode_reward

            if self._verbose and self._episodes % self._log_interval == 0:
                print(f"Episode {self._episodes} - Avg. Reward: {round(self._cumulative_reward / self._episodes, 2)}",
                      flush=True)

            self._episode_reward = 0.0

    def result(self):
        return self._cumulative_reward / self._episodes if self._episodes != 0 else 0.0

    def reset(self):
        self._episodes = 0
        self._cumulative_reward = 0.0
        self._episode_reward = 0.0
        self._average_episode_reward = 0.0
