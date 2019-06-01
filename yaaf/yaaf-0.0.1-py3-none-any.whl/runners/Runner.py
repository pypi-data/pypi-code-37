from abc import ABC, abstractmethod
from collections import namedtuple

from yaaf.agents.TrainableAgent import TrainableAgent

Timestep = namedtuple("Timestep", "state action reward next_state is_terminal info")


class Runner(ABC):
    # TODO - Progress using TQDM

    """
    Runner: An object which interacts an agent with an environment and notifies observers
    """

    def __init__(self, actor, environment, observers):
        """
        :param actor: The agent or the policy to interact with the environment
        :param environment: The environment
        :param observers: The observers
        """
        self._actor = actor
        self._environment = environment
        self._observers = observers or []

        self._total_steps = 0
        self._total_episodes = 0

    @property
    def total_steps(self):
        return self._total_steps

    @property
    def total_episodes(self):
        return self._total_episodes

    @abstractmethod
    def run(self):
        raise NotImplementedError()

    def step(self):
        state = self._environment.state
        action = self._actor.action(state)
        timestep = self._environment.step(action)
        for observer in self._observers:
            observer(timestep)
        if isinstance(self._actor, TrainableAgent):
            self._actor.reinforcement(timestep)
        self._total_steps += 1
        is_terminal = timestep.is_terminal
        if is_terminal:
            self._total_episodes += 1
        return timestep

    def episode(self):
        self._environment.reset()
        is_terminal = False
        trajectory = [self._environment.state]
        while not is_terminal:
            timestep = self.step()
            trajectory.append(timestep)
        return trajectory
