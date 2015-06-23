from prefs_n_perms.client import redis
from prefs_n_perms.permissions import Permissions
from prefs_n_perms.preferences import Preferences
from prefs_n_perms.settings import preference_settings


class Section(object):

    def __init__(self, name):
        self.name = name
        self.hierarchy_key = preference_settings.HIERARCHY_KEY
        self.preferences = Preferences(self)
        self.permissions = Permissions(self)

    def __str__(self):
        return self.name

    def get_hierarchy_key(self):
        return self.hierarchy_key.format(section=self.name)

    def exists(self):
        return redis.exists(self.get_hierarchy_key())

    def get_hierarchy(self):
        return redis.lrange(self.get_hierarchy_key(), 0, -1)

    def set_hierarchy(self, value):
        if not isinstance(value, (tuple, list)):
            raise ValueError
        redis.delete(self.get_hierarchy_key())
        redis.rpush(self.get_hierarchy_key(), *value)

    hierarchy = property(get_hierarchy, set_hierarchy)

    def has_preferences(self):
        return self.preferences.exists()

    def has_permissions(self):
        return self.permissions.exists()
