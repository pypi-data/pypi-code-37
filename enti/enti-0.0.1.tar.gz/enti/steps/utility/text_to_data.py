from enti.api import *

class TextToDataTransformer(Processor):

    def __init__(self, key):
        super(TextToDataTransformer, self).__init__(
            "text-to-data-transform",
            method=None
        )
        self.key = key

    def run(self, input, *args, **kwargs):
        output = {self.key: input}
        return output
