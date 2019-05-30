"""
"""


class LeakyReLUNeuron:
    def __init__(self, input, output):
        self._input = input
        self._output = output

        self._input.bind_to(self._update_input)
        self._update_input()

    def _update_input(self):
        if self._input.value > 0:
            self._output.value = self._input.value
        else:
            self._output.value = self._input.value*0.01


class LeakyReLULayer:
    def __init__(self, inputs, outputs):
        if len(outputs) != len(inputs):
            raise TypeError(
                "Expected {0} outputs, received {1}.".format(
                    len(inputs),
                    len(outputs)
                )
            )

        self._neurons = [LeakyReLUNeuron(inputs[i], outputs[i]) for i in range(len(inputs))]
