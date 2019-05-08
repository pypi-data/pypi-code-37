import logging
import pickle

logger = logging.getLogger(__name__)

try:
    import ujson as json
except ImportError:
    logger.warning("ujson module not found, using json")
    import json

try:
    import msgpack
except ImportError:
    logger.warning("msgpack not installed, MsgPackSerializer unavailable")


_NOT_SET = object()


class BaseSerializer:

    DEFAULT_ENCODING = "utf-8"

    def __init__(self, *args, encoding=_NOT_SET, **kwargs):
        self.encoding = self.DEFAULT_ENCODING if encoding is _NOT_SET else encoding
        super().__init__(*args, **kwargs)

    def dumps(self, value):
        raise NotImplementedError("dumps method must be implemented")

    def loads(self, value):
        raise NotImplementedError("loads method must be implemented")


class NullSerializer(BaseSerializer):
    """
    This serializer does nothing. Its only recommended to be used by
    :class:`pycached.SimpleMemoryCache` because for other backends it will
    produce incompatible data unless you work only with str types.

    DISCLAIMER: Be careful with mutable types and memory storage. The following
    behavior is considered normal (same as ``functools.lru_cache``)::

        cache = Cache()
        my_list = [1]
        cache.set("key", my_list)
        my_list.append(2)
        cache.get("key")  # Will return [1, 2]
    """

    def dumps(self, value):
        """
        Returns the same value
        """
        return value

    def loads(self, value):
        """
        Returns the same value
        """
        return value


class StringSerializer(BaseSerializer):
    """
    Converts all input values to str. All return values are also str. Be
    careful because this means that if you store an ``int(1)``, you will get
    back '1'.

    The transformation is done by just casting to str in the ``dumps`` method.

    If you want to keep python types, use ``PickleSerializer``. ``JsonSerializer``
    may also be useful to keep type of symple python types.
    """

    def dumps(self, value):
        """
        Serialize the received value casting it to str.

        :param value: obj Anything support cast to str
        :returns: str
        """
        return str(value)

    def loads(self, value):
        """
        Returns value back without transformations
        """
        return value


class PickleSerializer(BaseSerializer):
    """
    Transform data to bytes using pickle.dumps and pickle.loads to retrieve it back.
    """

    DEFAULT_ENCODING = None

    def dumps(self, value):
        """
        Serialize the received value using ``pickle.dumps``.

        :param value: obj
        :returns: bytes
        """
        return pickle.dumps(value)

    def loads(self, value):
        """
        Deserialize value using ``pickle.loads``.

        :param value: bytes
        :returns: obj
        """
        if value is None:
            return None
        return pickle.loads(value)


class JsonSerializer(BaseSerializer):
    """
    Transform data to json string with json.dumps and json.loads to retrieve it back. Check
    https://docs.python.org/3/library/json.html#py-to-json-table for how types are converted.

    ujson will be used by default if available. Be careful with differences between built in
    json module and ujson:
        - ujson dumps supports bytes while json doesn't
        - ujson and json outputs may differ sometimes
    """

    def dumps(self, value):
        """
        Serialize the received value using ``json.dumps``.

        :param value: dict
        :returns: str
        """
        return json.dumps(value)

    def loads(self, value):
        """
        Deserialize value using ``json.loads``.

        :param value: str
        :returns: output of ``json.loads``.
        """
        if value is None:
            return None
        return json.loads(value)


class MsgPackSerializer(BaseSerializer):
    """
    Transform data to bytes using msgpack.dumps and msgpack.loads to retrieve it back. You need
    to have ``msgpack`` installed in order to be able to use this serializer.

    :param encoding: str. Can be used to change encoding param for ``msg.loads`` method.
        Default is utf-8.
    :param use_list: bool. Can be used to change use_list param for ``msgpack.loads`` method.
        Default is True.
    """

    def __init__(self, *args, use_list=True, **kwargs):
        self.use_list = use_list
        super().__init__(*args, **kwargs)

    def dumps(self, value):
        """
        Serialize the received value using ``msgpack.dumps``.

        :param value: obj
        :returns: bytes
        """
        return msgpack.dumps(value)

    def loads(self, value):
        """
        Deserialize value using ``msgpack.loads``.

        :param value: bytes
        :returns: obj
        """
        if value is None:
            return None
        return msgpack.loads(value, encoding=self.encoding, use_list=self.use_list)
