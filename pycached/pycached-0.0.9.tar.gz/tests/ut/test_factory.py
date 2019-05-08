from unittest.mock import patch

import pytest

from pycached import SimpleMemoryCache, RedisCache, caches, Cache
from pycached.exceptions import InvalidCacheType
from pycached.factory import _class_from_string, _create_cache
from pycached.plugins import TimingPlugin, HitMissRatioPlugin
from pycached.serializers import JsonSerializer, PickleSerializer


def test_class_from_string():
    assert _class_from_string("pycached.RedisCache") == RedisCache


def test_create_simple_cache():
    redis = _create_cache(RedisCache, endpoint="127.0.0.10", port=6378)

    assert isinstance(redis, RedisCache)
    assert redis.endpoint == "127.0.0.10"
    assert redis.port == 6378


def test_create_cache_with_everything():
    redis = _create_cache(
        RedisCache,
        serializer={"class": PickleSerializer, "encoding": "encoding"},
        plugins=[{"class": "pycached.plugins.TimingPlugin"}],
    )

    assert isinstance(redis.serializer, PickleSerializer)
    assert redis.serializer.encoding == "encoding"
    assert isinstance(redis.plugins[0], TimingPlugin)


class TestCache:
    def test_cache_types(self):
        assert Cache.MEMORY == "memory"
        assert Cache.REDIS == "redis"

    @pytest.mark.parametrize("cache_type", [Cache.MEMORY, Cache.REDIS])
    def test_new(self, cache_type):
        kwargs = {"a": 1, "b": 2}
        cache_class = Cache.get_protocol_class(cache_type)

        with patch("pycached.{}.__init__".format(cache_class.__name__)) as init:
            cache = Cache(cache_type, **kwargs)
            assert isinstance(cache, cache_class)
            init.assert_called_once_with(**kwargs)

    def test_new_defaults_to_memory(self):
        assert isinstance(Cache(), Cache.get_protocol_class(Cache.MEMORY))

    def test_new_invalid_cache_raises(self):
        with pytest.raises(InvalidCacheType) as e:
            Cache("file")
        assert str(e.value) == "Invalid cache type, you can only use {}".format(
            list(Cache._PROTOCOL_MAPPING.keys())
        )

    @pytest.mark.parametrize("protocol", [Cache.MEMORY, Cache.REDIS])
    def test_get_protocol_class(self, protocol):
        assert Cache.get_protocol_class(protocol) == Cache._PROTOCOL_MAPPING[protocol]

    def test_get_protocol_class_invalid(self):
        with pytest.raises(KeyError):
            Cache.get_protocol_class("http")


class TestCacheHandler:
    @pytest.fixture(autouse=True)
    def remove_caches(self):
        caches._caches = {}

    def test_get_wrong_alias(self):
        with pytest.raises(KeyError):
            caches.get("wrong_cache")

        with pytest.raises(KeyError):
            caches.create("wrong_cache")

    def test_reuse_instance(self):
        assert caches.get("default") is caches.get("default")

    def test_create_not_reuse(self):
        assert caches.create("default") is not caches.create("default")

    def test_create_extra_args(self):
        caches.set_config(
            {
                "default": {
                    "cache": "pycached.RedisCache",
                    "endpoint": "127.0.0.9",
                    "db": 10,
                    "port": 6378,
                }
            }
        )
        cache = caches.create("default", namespace="whatever", endpoint="127.0.0.10", db=10)
        assert cache.namespace == "whatever"
        assert cache.endpoint == "127.0.0.10"
        assert cache.db == 10

    def test_retrieve_cache(self):
        caches.set_config(
            {
                "default": {
                    "cache": "pycached.RedisCache",
                    "endpoint": "127.0.0.10",
                    "port": 6378,
                    "ttl": 10,
                    "serializer": {
                        "class": "pycached.serializers.PickleSerializer",
                        "encoding": "encoding",
                    },
                    "plugins": [
                        {"class": "pycached.plugins.HitMissRatioPlugin"},
                        {"class": "pycached.plugins.TimingPlugin"},
                    ],
                }
            }
        )

        cache = caches.get("default")
        assert isinstance(cache, RedisCache)
        assert cache.endpoint == "127.0.0.10"
        assert cache.port == 6378
        assert cache.ttl == 10
        assert isinstance(cache.serializer, PickleSerializer)
        assert cache.serializer.encoding == "encoding"
        assert len(cache.plugins) == 2

    def test_retrieve_cache_new_instance(self):
        caches.set_config(
            {
                "default": {
                    "cache": "pycached.RedisCache",
                    "endpoint": "127.0.0.10",
                    "port": 6378,
                    "serializer": {
                        "class": "pycached.serializers.PickleSerializer",
                        "encoding": "encoding",
                    },
                    "plugins": [
                        {"class": "pycached.plugins.HitMissRatioPlugin"},
                        {"class": "pycached.plugins.TimingPlugin"},
                    ],
                }
            }
        )

        cache = caches.create("default")
        assert isinstance(cache, RedisCache)
        assert cache.endpoint == "127.0.0.10"
        assert cache.port == 6378
        assert isinstance(cache.serializer, PickleSerializer)
        assert cache.serializer.encoding == "encoding"
        assert len(cache.plugins) == 2

    def test_create_cache_str_no_alias(self):
        cache = caches.create(cache="pycached.RedisCache")

        assert isinstance(cache, RedisCache)
        assert cache.endpoint == "127.0.0.1"
        assert cache.port == 6379

    def test_create_cache_class_no_alias(self):
        cache = caches.create(cache=RedisCache)

        assert isinstance(cache, RedisCache)
        assert cache.endpoint == "127.0.0.1"
        assert cache.port == 6379

    def test_create_cache_ensure_alias_or_cache(self):
        with pytest.raises(TypeError):
            caches.create()

    def test_alias_config_is_reusable(self):
        caches.set_config(
            {
                "default": {
                    "cache": "pycached.RedisCache",
                    "endpoint": "127.0.0.10",
                    "port": 6378,
                    "serializer": {"class": "pycached.serializers.PickleSerializer"},
                    "plugins": [
                        {"class": "pycached.plugins.HitMissRatioPlugin"},
                        {"class": "pycached.plugins.TimingPlugin"},
                    ],
                },
                "alt": {"cache": "pycached.SimpleMemoryCache"},
            }
        )

        default = caches.create(**caches.get_alias_config("default"))
        alt = caches.create(**caches.get_alias_config("alt"))

        assert isinstance(default, RedisCache)
        assert default.endpoint == "127.0.0.10"
        assert default.port == 6378
        assert isinstance(default.serializer, PickleSerializer)
        assert len(default.plugins) == 2

        assert isinstance(alt, SimpleMemoryCache)

    def test_multiple_caches(self):
        caches.set_config(
            {
                "default": {
                    "cache": "pycached.RedisCache",
                    "endpoint": "127.0.0.10",
                    "port": 6378,
                    "serializer": {"class": "pycached.serializers.PickleSerializer"},
                    "plugins": [
                        {"class": "pycached.plugins.HitMissRatioPlugin"},
                        {"class": "pycached.plugins.TimingPlugin"},
                    ],
                },
                "alt": {"cache": "pycached.SimpleMemoryCache"},
            }
        )

        default = caches.get("default")
        alt = caches.get("alt")

        assert isinstance(default, RedisCache)
        assert default.endpoint == "127.0.0.10"
        assert default.port == 6378
        assert isinstance(default.serializer, PickleSerializer)
        assert len(default.plugins) == 2

        assert isinstance(alt, SimpleMemoryCache)

    def test_default_caches(self):
        assert caches.get_config() == {
            "default": {
                "cache": "pycached.SimpleMemoryCache",
                "serializer": {"class": "pycached.serializers.NullSerializer"},
            }
        }

    def test_get_alias_config(self):
        assert caches.get_alias_config("default") == {
            "cache": "pycached.SimpleMemoryCache",
            "serializer": {"class": "pycached.serializers.NullSerializer"},
        }

    def test_set_empty_config(self):
        with pytest.raises(ValueError):
            caches.set_config({})

    def test_set_config_updates_existing_values(self):
        assert not isinstance(caches.get("default").serializer, JsonSerializer)
        caches.set_config(
            {
                "default": {
                    "cache": "pycached.SimpleMemoryCache",
                    "serializer": {"class": "pycached.serializers.JsonSerializer"},
                }
            }
        )
        assert isinstance(caches.get("default").serializer, JsonSerializer)

    def test_set_config_removes_existing_caches(self):
        caches.set_config(
            {
                "default": {"cache": "pycached.SimpleMemoryCache"},
                "alt": {"cache": "pycached.SimpleMemoryCache"},
            }
        )
        caches.get("default")
        caches.get("alt")
        assert len(caches._caches) == 2

        caches.set_config(
            {
                "default": {"cache": "pycached.SimpleMemoryCache"},
                "alt": {"cache": "pycached.SimpleMemoryCache"},
            }
        )
        assert caches._caches == {}

    def test_set_config_no_default(self):
        with pytest.raises(ValueError):
            caches.set_config(
                {
                    "no_default": {
                        "cache": "pycached.RedisCache",
                        "endpoint": "127.0.0.10",
                        "port": 6378,
                        "serializer": {"class": "pycached.serializers.PickleSerializer"},
                        "plugins": [
                            {"class": "pycached.plugins.HitMissRatioPlugin"},
                            {"class": "pycached.plugins.TimingPlugin"},
                        ],
                    }
                }
            )

    def test_ensure_plugins_order(self):
        caches.set_config(
            {
                "default": {
                    "cache": "pycached.RedisCache",
                    "plugins": [
                        {"class": "pycached.plugins.HitMissRatioPlugin"},
                        {"class": "pycached.plugins.TimingPlugin"},
                    ],
                }
            }
        )

        cache = caches.get("default")
        assert isinstance(cache.plugins[0], HitMissRatioPlugin)

        cache = caches.create("default")
        assert isinstance(cache.plugins[0], HitMissRatioPlugin)
