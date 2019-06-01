from yaaf.metrics.Metric import Metric


class AverageTimestepReward(Metric):

    def __init__(self, verbose=False, log_interval=1):
        super(AverageTimestepReward, self).__init__("Average Timestep Reward")

        if verbose:
            assert log_interval is not None, f"{self.name} requires a log_interval when verbose."
        self._verbose = verbose
        self._log_interval = log_interval

        self._timesteps = 0
        self._cumulative_reward = 0.0
        self._average_reward = 0.0

    @property
    def name(self):
        return self._name

    def __call__(self, timestep):
        reward = timestep.reward
        self._cumulative_reward += reward
        self._timesteps += 1
        if self._verbose and self._timesteps % self._log_interval == 0:
            print(f"Timestep {self._timesteps} - Avg. Reward: {round(self._cumulative_reward / self._timesteps, 4)}",
                  flush=True)

    def result(self):
        return self._cumulative_reward / self._timesteps if self._timesteps != 0 else 0.0

    def reset(self):
        self._timesteps = 0
        self._cumulative_reward = 0.0
        self._average_reward = 0.0
