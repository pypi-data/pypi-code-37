from yaaf.agents.Agent import Agent
from yaaf.policies.RandomPolicy import RandomPolicy


class RandomAgent(Agent):

    def __init__(self, action_space, name="Random"):
        super().__init__(name, RandomPolicy(action_space))
