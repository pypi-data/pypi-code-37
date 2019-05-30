"""
"""

import neuron


class FullyConnectedLayer:
    def __init__(self, inputs, outputs):
        self._neurons = [Neuron(inputs, output) for output in outputs]
