import logging

logger = logging.getLogger(__name__)
import time
import threading
import redis
from rediscluster import StrictRedisCluster


class IdGenerator:
    """
    全局id生成器
    id组成： 时间+业务字段（最长四个字符）+实例ID+进程内自增
    """
    def __init__(self, biz_name, redis_host, redis_port, redis_password, redis_db, redis_nodes):
        self._biz_name = biz_name
        self._last_timestamp = time.time()
        self._instance_id = self.__get_current_instance_id(biz_name=biz_name, redis_host=redis_host,
                                                           redis_port=redis_port, redis_password=redis_password,
                                                           redis_db=redis_db, redis_nodes=redis_nodes)
        self._value_lock = threading.Lock()
        self._incr = 0

    def __get_current_instance_id(self, biz_name, redis_host, redis_port, redis_password, redis_db, redis_nodes):
        """
        获取实例id，通过redis incr 微服务名称 key获取当前实例id
        :param biz_name: 所属微服务名称
        :param redis_host:
        :param redis_port:
        :param redis_password:
        :param redis_db:
        :return: 实例id
        """
        client = None
        if redis_nodes is not None:
            client = StrictRedisCluster(startup_nodes=redis_nodes)
        else:
            client = redis.Redis(host=redis_host, port=redis_port, password=redis_password, db=redis_db)
        key = 'IdGenerator:' + biz_name
        value = client.incr(key)
        client.expire(key, 3600)
        return value

    def uuid(self, name):
        """
        获取uuid
        :param name: 业务名称，不超过4个字符
        :return: uuid
        """
        if name is None or len(name) > 4 or len(name.strip()) < 1:
            raise Exception('name must be not empty and the length should be less than 4')
        # 锁，对比上次时间戳与这次时间戳，防止机器时间同步导致时间退后导致重复ID
        with self._value_lock:
            timestamp = time.time()
            if timestamp < self._last_timestamp:
                logger.error("Time moved backforward. current: %d, last: %d", timestamp, self._last_timestamp)
                timestamp = self._last_timestamp
            self._incr += 1
            return "%s%s%d%08d" % (time.strftime("%Y%m%d%H%M%S", time.localtime(int(timestamp))), name, self._instance_id, self._incr % 100000000)


class Properties:
    """
    读取properties文件工具类
    注意，这里的properties的value内容不支持换行
    """
    def __init__(self, file_name):
        self.file_name = file_name
        self.properties = {}
        try:
            fopen = open(self.file_name, 'r')
            for line in fopen:
                line = line.strip()
                if line.find('=') > 0 and not line.startswith('#'):
                    strs = line.split('=')
                    self.properties[strs[0].strip()] = strs[1].strip()
        except Exception as e:
            raise e
        else:
            fopen.close()

    def has_key(self, key):
        """
        判断是否包含key
        :param key:
        :return:
        """
        return key in self.properties

    def get(self, key, default_value=''):
        """
        获取key，不存在则返回default_value
        :param key:
        :param default_value:
        :return:
        """
        if key in self.properties:
            return self.properties[key]
        return default_value
