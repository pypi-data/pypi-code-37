import math

from yaaf.runners.Runner import Runner


class BottleneckRunner(Runner):

    def __init__(self, agent, environment, timesteps=math.inf, episodes=math.inf, observers=None):
        super(BottleneckRunner, self).__init__(agent, environment, observers)
        self._timesteps = timesteps
        self._episodes = episodes

    def run(self):
        self._environment.reset()
        done = False
        while not done:
            self.step()
            done = self.total_episodes >= self._episodes or self.total_steps >= self._timesteps
