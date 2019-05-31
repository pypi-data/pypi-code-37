from pluckit import Pluckable
from rekey import Rekeyable
from sqlalchemy.orm.collections import MappedCollection


class ResultList(list, Pluckable, Rekeyable):
    def __lshift__(self, other):
        self.append(other)
        return other


class ResultDict(MappedCollection, Pluckable, Rekeyable):
    def __init__(self, *args, **kw):
        MappedCollection.__init__(self, keyfunc=self.key_for)

    @staticmethod
    def key_for(obj):
        key = list(obj.__table__.primary_key)
        assert len(key) == 1
        return getattr(obj, key[0].name)

    def __lshift__(self, other):
        self[self.key_for(other)] = other
        return other



class ResultSet(dict, Pluckable, Rekeyable): pass
