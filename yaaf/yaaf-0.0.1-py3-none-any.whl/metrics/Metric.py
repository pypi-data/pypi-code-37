from abc import abstractmethod, ABC

from yaaf.runners.Runner import Timestep


class Metric(ABC):

    def __init__(self, name):
        self._name = name

    @abstractmethod
    def reset(self):
        raise NotImplementedError()

    @abstractmethod
    def __call__(self, timestep: Timestep):
        raise NotImplementedError()

    def result(self):
        raise NotImplementedError()
