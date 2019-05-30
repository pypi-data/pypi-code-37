"""
"""


class Connection:
    def __init__(self, value=0):
        self._value = value
        self._connections = []

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value != self._value:
            self._value = value
            for callback in self._connections:
                callback()

    def bind_to(self, callback):
        if callback not in self._connections:
            self._connections.append(callback)
