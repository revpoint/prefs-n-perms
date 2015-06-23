from prefs_n_perms.client import redis
from prefs_n_perms.permissions import Permissions
from prefs_n_perms.preferences import Preferences
from prefs_n_perms.settings import preference_settings


class Section(object):

    def __init__(self, name):
        self.name = name
        self.prefix = preference_settings.SECTIONS_PREFIX
        self.preferences = Preferences(self)
        self.permissions = Permissions(self)

    def __str__(self):
        return self.name

    def get_key(self):
        return ':'.join((self.prefix, self.name))

    def exists(self):
        return redis.exists(self.get_key())

    def has_preferences(self):
        return self.preferences.exists()

    def has_permissions(self):
        return self.permissions.exists()

    @property
    def tiers(self):
        return redis.lrange(self.get_key(), 0, -1)

    @tiers.setter
    def tiers(self, value):
        if not isinstance(value, (tuple, list)):
            raise ValueError
        redis.delete(self.get_key())
        redis.rpush(self.get_key(), *value)
