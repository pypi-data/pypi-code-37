class ConfigNamespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        keys = sorted(self.__dict__)
        items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys)
        return "{}({})".format(type(self).__name__, ", ".join(items))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def update(self, other):
        if isinstance(other, ConfigNamespace):
            self.__dict__.update(other.__dict__)
        elif isinstance(other, dict):
            self.__dict__.update(other)