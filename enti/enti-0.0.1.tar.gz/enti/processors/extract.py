import re
from enti.api.processor import *
from enti.api.entity import Entity

__all__ = [
    "LexiconExtractor"
]

class LexiconExtractor(Processor):

    def __init__(self, lexicon, input_key, output_key):
        super(LexiconExtractor, self).__init__(
            "lexicon-extract"
        )
        self.key = input_key
        self.target = output_key
        self.lexicon = lexicon

        for e in lexicon:
            if not isinstance(e, Entity):
                raise Exception(f"Invalid lexicon: Element {e!r} is not an <Entity>")

    def run(self, data, *args, **kwargs):
        text = data[self.key]
        if not data.get(self.target):
            data[self.target] = {}
        for entity in self.lexicon:
            matched_entities = entity.search(text)
            for e in matched_entities:
                if not data[self.target].get(entity.type):
                    data[self.target][entity.type] = []
                data[self.target][entity.type].append(e.properties)
        return data

