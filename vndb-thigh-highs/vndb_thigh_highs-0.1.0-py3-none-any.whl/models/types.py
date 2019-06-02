_identity = lambda x: x

BOOLEAN = _identity
DATE = _identity
INTEGER = _identity
TIMESTAMP = _identity
STRING = _identity

class JoinedStrings:
    def __init__(self, separator="\n"):
        self.separator = separator

    def __call__(self, string):
        return string.split(self.separator)

class ListOf:
    def __init__(self, field_type):
        self.field_type = field_type

    def __call__(self, objs):
        return [self.field_type(obj) for obj in objs]
