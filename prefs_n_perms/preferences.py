from prefs_n_perms.client import redis
from prefs_n_perms.settings import preference_settings


class Preferences(object):

    def __init__(self, section):
        self.section = section
        self.preferences_key = preference_settings.PREFERENCES_KEY

    def get_preferences_key(self):
        return self.preferences_key.format(section=self.section.name)

    def get_key_for(self, entity):
        return ':'.join((self.get_preferences_key(), entity))

    def exists(self):
        return redis.exists(self.get_key_for('global'))

    def get_all(self, **kwargs):
        prefs = redis.hgetall(self.get_key_for('global'))
        for entity in self.section.hierarchy:
            if entity in kwargs:
                key = '.'.join((entity, kwargs['hier']))
                prefs.update(redis.hgetall(self.get_key_for(key)))
        return prefs

    def get_pref(self, name, **kwargs):
        pref = redis.hget(self.get_key_for('global'), name)
        for entity in self.section.hierarchy:
            if entity in kwargs:
                key = '.'.join((entity, kwargs['hier']))
                value = redis.hget(self.get_key_for(key), name)
                if value:
                    pref = value
        return pref
