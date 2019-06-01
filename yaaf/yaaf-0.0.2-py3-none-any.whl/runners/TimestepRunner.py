from yaaf.runners.BottleneckRunner import BottleneckRunner


class TimestepRunner(BottleneckRunner):
    def __init__(self, actor, environment, timesteps, observers=None):
        super(TimestepRunner, self).__init__(actor, environment, timesteps=timesteps, observers=observers)
