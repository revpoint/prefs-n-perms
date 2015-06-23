from prefs_n_perms.client import redis
from prefs_n_perms.settings import preference_settings


class Permissions(object):

    def __init__(self, section):
        self.section = section
        self.prefix = preference_settings.PERMISSIONS_PREFIX
        self.available_key = self.key_for('available')

    def key_for(self, entity):
        return ':'.join((self.prefix, self.section.name, entity))

    def exists(self):
        return redis.exists(self.available_key)

    def get_available_permissions(self):
        return redis.smembers(self.available_key)
