import pathlib
from abc import ABC, abstractmethod


class Model(ABC):

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def save(self, directory):
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        self._save(directory)

    @abstractmethod
    def _save(self, directory):
        raise NotImplementedError()

    @abstractmethod
    def load(self, directory):
        raise NotImplementedError()
