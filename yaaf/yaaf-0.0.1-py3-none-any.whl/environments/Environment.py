from abc import ABC, abstractmethod


class Environment(ABC):

    def __init__(self, name, observation_space, action_space, render):
        self._name = name
        self._observation_space = observation_space
        self._action_space = action_space
        self._should_render = render
        self._state = None
        self._is_terminal = True

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def observation_space(self):
        return self._observation_space

    @property
    def action_space(self):
        return self._action_space

    @property
    def terminal(self):
        return self._is_terminal

    def reset(self):
        self._state = self._reset()
        self._is_terminal = False
        if self._should_render:
            self._render()
        return self._state

    def step(self, action):

        assert 0 <= action <= self.action_space, self.describe_actions()

        if self._is_terminal:
            self._state = self.reset()

        timestep = self._step(action)

        self._state = timestep.next_state
        self._is_terminal = timestep.is_terminal

        if self._should_render:
            self._render()

        return timestep

    @abstractmethod
    def _reset(self):
        raise NotImplementedError()

    @abstractmethod
    def _step(self, action):
        raise NotImplementedError()

    @abstractmethod
    def _render(self):
        raise NotImplementedError()

    def describe_actions(self):
        description = "Actions:"
        for a in range(self.action_space):
            description += f"[{a}]: {self.describe_action(a)}"

    @abstractmethod
    def describe_action(self, a):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()
