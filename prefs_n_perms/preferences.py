from prefs_n_perms.client import redis
from prefs_n_perms.settings import preference_settings


class Preferences(object):
    def __init__(self, section):
        self.section = section
        self.prefix = preference_settings.PREFERENCES_PREFIX
        self.global_key = self.key_for('global')

    def key_for(self, entity):
        return ':'.join((self.prefix, self.section.name, entity))

    def exists(self):
        return redis.exists(self.global_key)

    def get_global_prefs(self):
        return redis.hgetall(self.global_key)

    def get_global_pref(self, name):
        return redis.hget(self.global_key, name)


class BoundedPreferences(object):
    def __init__(self, preferences, instances):
        self.preferences = preferences
        self.instances = instances

    def key_for(self, entity):
        return self.preferences.key_for(entity)

    def get_instance_keys(self):
        return dict((k, '.'.join((k, v))) for k, v in self.instances.iteritems())

    def get_combined_prefs(self):
        prefs = self.preferences.get_global_prefs()
        instance_keys = self.get_instance_keys()
        for tier in self.preferences.section.tiers:
            if tier in instance_keys:
                instance = instance_keys[tier]
                prefs.update(redis.hgetall(self.key_for(instance)))
        return prefs

    def get_combined_pref(self, name):
        pref = self.preferences.get_global_pref(name)
        instance_keys = self.get_instance_keys()
        for tier in self.preferences.section.tiers:
            if tier in instance_keys:
                instance = instance_keys[tier]
                value = redis.hget(self.key_for(instance), name)
                if value:
                    pref = value
        return pref
