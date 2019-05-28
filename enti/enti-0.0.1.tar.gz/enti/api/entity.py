from uuid import uuid4
from enti.api.regex import *
import re




class Entity:
    ACTION = "ACT"
    OBJECT = "OBJ"
    LOCATION = "LOC"
    ORGANIZATION = "ORG"
    PERSON = "P"
    PEOPLE = "PP"
    LIST = "LIST"
    TITLE = "TITLE"

    def __init__(self, type, pattern, label, pos=None, attributes=None, case_insensitive=False):
        self.id = str(uuid4()).upper()
        self.type = type
        self.label = label
        self.attributes = attributes if attributes is not None else {}
        self.pattern = _re_(pattern)
        if case_insensitive:
            self.pattern = re.compile(self.pattern.pattern, re.I)
        self.pos = pos
        self.attributes = attributes
        self.case_insensitive = case_insensitive

    def search(self, text):
        return [MatchedEntity(self, m, text) for m in re.finditer(self.pattern, text)]

    @property
    def properties(self):
        return {
            "type": self.type,
            "label": self.label,
            "attributes": self.attributes,
            "pos": self.pos
        }
    @staticmethod
    def build_list(partials, entity_type, transform=None, pos=None, attributes=None):

        _transform = transform
        if _transform is None:
            _transform = lambda x: x
        _attrs = attributes if attributes is not None else {}

        return [Entity(
            type=entity_type,
            label=p.label,
            pattern=(_re_(_transform(p.pattern))),
            pos=pos,
            attributes=attributes
        )
            for p in partials
        ]

    class Partial:
        def __init__(self, label, alts=None, attributes=None):

            alt = alts
            if alt is None:
                alt = []
            self.pattern = _jo_([label] + alt)
            self.label = _sp_p_(label)
            self.attributes = attributes

    class Extractor:
        def __init__(self, pattern, attributes):
            self.pattern = pattern
            self.attributes = attributes


class MatchedEntity(Entity):
    def __init__(self, entity, match, text):
        super(MatchedEntity, self).__init__(
            entity.type, entity.pattern, entity.label,
            entity.pos, entity.attributes, entity.case_insensitive
        )
        self.span = match.span()
        self.value = text[self.span[0]:self.span[1]]

    @property
    def properties(self):
        return {
            "type": self.type,
            "label": self.label,
            "attributes": self.attributes,
            "pos": self.pos,
            "value": self.value
        }
