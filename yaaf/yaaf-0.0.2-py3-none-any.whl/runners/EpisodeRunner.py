from yaaf.runners.BottleneckRunner import BottleneckRunner


class EpisodeRunner(BottleneckRunner):
    def __init__(self, agent, environment, episodes, observers=None):
        super(EpisodeRunner, self).__init__(agent, environment, episodes=episodes, observers=observers)
