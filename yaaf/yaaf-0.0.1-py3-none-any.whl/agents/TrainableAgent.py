import pathlib
from abc import ABC, abstractmethod

from yaaf.agents.Agent import Agent


class TrainableAgent(Agent, ABC):

    def __init__(self, name, evaluation_policy, training_policy, train, load_from):
        super(TrainableAgent, self).__init__(name, evaluation_policy)
        self._training = train
        self._policy = training_policy if train else evaluation_policy
        self._training_policy = training_policy
        self._evaluation_policy = evaluation_policy
        if load_from is not None:
            self.load(load_from)

    def enable_training(self):
        self._training = True
        self._policy = self._training_policy

    def disable_training(self):
        self._training = False
        self._policy = self._evaluation_policy

    def reinforcement(self, timestep):
        if not self._training:
            return
        else:
            self._reinforce(timestep)

    @abstractmethod
    def _reinforce(self, timestep):
        raise NotImplementedError()

    def save(self, directory):
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        self._save(directory)

    @abstractmethod
    def _save(self, directory):
        raise NotImplementedError()

    @abstractmethod
    def load(self, directory):
        raise NotImplementedError()
