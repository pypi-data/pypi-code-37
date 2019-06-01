import gym
import numpy as np
from numpy.core.multiarray import ndarray

from yaaf.environments.Environment import Environment
from yaaf.runners.Runner import Timestep


class OpenAIGymEnvironment(Environment):

    def __init__(self, name, render=False):
        self._openai_env = gym.make(name)
        observation_space = self._openai_env.observation_space.shape
        if observation_space == ():
            observation_space = (1,)
        super().__init__(name, observation_space, self._openai_env.action_space.n, render)
        self._is_open = True

    def _reset(self):
        if not self._is_open:
            self._openai_env = gym.make(self.name)
        return self._openai_env.reset().reshape(self.observation_space)

    def _step(self, action):
        observation, reward, done, info = self._openai_env.step(action)
        if not isinstance(observation, ndarray):
            observation = np.array([observation]).reshape(self.observation_space)
        timestep = Timestep(self._state, action, reward, observation, done, info)
        return timestep

    def _render(self):
        return self._openai_env.render()

    def describe_actions(self):
        return f"See https://gym.openai.com/envs/{self.name}/ for info on available actions."

    def describe_action(self, a):
        # Overwritten describe_actions
        pass

    def close(self):
        self._openai_env.close()
        self._is_open = False
