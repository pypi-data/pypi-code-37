import redis

from pyapp.conf.helpers import NamedFactory

__all__ = ("client_factory", "get_client")


class RedisFactory(NamedFactory[redis.Redis]):
    """
    Redis factory
    """

    required_keys = ("url",)
    optional_keys = (
        "host",
        "port",
        "db",
        "password",
        "socket_timeout",
        "socket_connect_timeout",
        "socket_keepalive",
        "socket_keepalive_options",
        "connection_pool",
        "unix_socket_path",
        "encoding",
        "encoding_errors",
        "charset",
        "errors",
        "decode_responses",
        "retry_on_timeout",
        "ssl",
        "ssl_keyfile",
        "ssl_certfile",
        "ssl_cert_reqs",
        "ssl_ca_certs",
        "max_connections",
    )

    def create(self, name: str = None) -> redis.Redis:
        config = self.get(name)
        return redis.Redis.from_url(**config)


client_factory = RedisFactory("REDIS")
get_client = client_factory.create
