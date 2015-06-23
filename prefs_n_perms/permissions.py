from prefs_n_perms.client import redis
from prefs_n_perms.settings import preference_settings


class Permissions(object):

    def __init__(self, section):
        self.section = section
        self.permissions_key = preference_settings.PERMISSIONS_KEY

    def get_permissions_key(self):
        return self.permissions_key.format(section=self.section.name)

    def get_key_for(self, entity):
        return ':'.join((self.get_permissions_key(), entity))

    def exists(self):
        return redis.exists(self.get_key_for('available'))
