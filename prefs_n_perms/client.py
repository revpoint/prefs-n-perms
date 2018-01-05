from prefs_n_perms import pool
from redish.client import Client
from redish.serialization import Plain
from prefs_n_perms.settings import preference_settings as settings


def get_client(url=None):
    connection_factory = pool.get_connection_factory()
    return connection_factory.connect(url or settings.REDIS_URL)


redis = get_client()


class RedishClient(Client):
    serializer = Plain()

    def __init__(self, *args, **kwargs):
        self.api = redis


db = RedishClient()
