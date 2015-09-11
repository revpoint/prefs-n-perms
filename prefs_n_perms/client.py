import redis as _redis
from redish.client import Client
from redish.serialization import Plain
from prefs_n_perms.settings import preference_settings


def get_connection_pool(url=None, **kwargs):
    return _redis.ConnectionPool.from_url(url or preference_settings.REDIS_URL, **kwargs)


def get_client(url=None, **kwargs):
    return _redis.StrictRedis(connection_pool=get_connection_pool(url, **kwargs))


redis = get_client()

class RedishClient(Client):
    serializer = Plain()

    def __init__(self, *args, **kwargs):
        self.api = redis


db = RedishClient()
