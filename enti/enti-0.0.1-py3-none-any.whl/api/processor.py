__all__ = [
    "Processor", "Mapper", "Pipeline"
]
from enti.debugging import debug

class Processor:
    def __init__(self, id, method=None, params=None, debug_level=2, mute=False):
        self.id = id
        self.method = method
        self.params = params if params is not None else {}
        self.debug_level = debug_level
        self.muted = mute

    def mute(self):
        self.muted = True

    def unmute(self):
        self.muted = False

    def set_debug_level(self, level):
        self.debug_level = level

    def __call__(self, *args, **kwargs):
        if not isinstance(self, Mapper):
            debug(f"[{self.id}]", depth=self.debug_level)
        output = self.run(*args, **kwargs)
        if not isinstance(self, Mapper) and not self.muted:
            debug(data=output, depth=self.debug_level)
        return output

    def run(self, data, *args, **kwargs):
        output = self.method(data, *args, **kwargs, **self.params)
        return output


class Mapper(Processor):
    def __init__(self, input_key, processor: Processor, output_key=None, mute=False):
        super(Mapper, self).__init__(id=f"mapper:{processor.id}")
        self.input_key = input_key
        self.output_key = (
            output_key if output_key is not None else input_key
        )
        self.processor = processor
        if mute:
            self.mute()

    def mute(self):
        self.muted = True
        self.processor.mute()

    def unmute(self):
        self.muted = False
        self.processor.unmute()

    def set_debug_level(self, level):
        self.debug_level = level + 1
        self.processor.set_debug_level(level + 2)

    def __call__(self, *args, **kwargs):
        debug(f"[{self.processor.id}] "
              f"({self.input_key}) => "
              f"({self.output_key})", depth=self.debug_level)
        output = self.run(*args, **kwargs)
        # debug(f"[{self.id}]", data=output, depth=self.debug_level)
        return output

    def run(self, data, *args, **kwargs):
        input = data[self.input_key]
        output = self.processor(input, *args, **kwargs)
        data[self.output_key] = output
        return data


class Pipeline(Processor):

    def __init__(self, id, steps, debug_level=1, mute=False):
        super(Pipeline, self).__init__(id)
        self.id = id
        self.processors = steps if isinstance(steps, list) else [steps]
        self.debug_level = debug_level
        self.set_debug_level(debug_level)
        if mute:
            self.mute()

    def mute(self):
        self.muted = True
        for processor in self.processors:
            processor.mute()

    def set_debug_level(self, level):
        self.debug_level = level
        for processor in self.processors:
            processor.set_debug_level(
                self.debug_level + 1
            )
            if self.mute:
                processor.muted = True

    def run(self, data, *args, **kwargs):
        output = data
        for step in self.processors:
            output = step(output, *args, **kwargs)
        return output

    def __call__(self, data, *args, **kwargs):
        return self.run(data, *args, **kwargs)