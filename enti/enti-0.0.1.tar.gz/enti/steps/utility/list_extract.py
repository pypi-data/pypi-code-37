from enti.api.processor import *

class ListExtractor(Processor):

    def __init__(self, key, index, target):
        super(ListExtractor, self).__init__(
            "list-extract"
        )
        self.key = key
        self.index = index
        self.target = target

    def run(self, data, *args, **kwargs):
        item = data[self.key][self.index]
        data[self.target] = item
        return data
