from prefs_n_perms.client import db
from prefs_n_perms.permissions import Permissions
from prefs_n_perms.preferences import Preferences
from prefs_n_perms.settings import preference_settings


class Section(object):
    prefix = preference_settings.SECTIONS_PREFIX

    def __init__(self, name, **kwargs):
        self.name = name
        self.preferences = Preferences(self, **kwargs)
        self.permissions = Permissions(self, **kwargs)

    def __str__(self):
        return self.name

    @property
    def section_key(self):
        return ':'.join((self.prefix, self.name))

    def exists(self):
        return self.section_key in db

    def has_preferences(self):
        return self.preferences.exists()

    def has_permissions(self):
        return self.permissions.exists()

    @property
    def tiers(self):
        return db.List(self.section_key)

    @tiers.setter
    def tiers(self, value):
        if not isinstance(value, (tuple, list)):
            raise ValueError
        del db[self.section_key]
        db.List(self.section_key, value)

    def load_data(self, **kwargs):
        self.preferences.load_data(**kwargs)
        self.permissions.load_data(**kwargs)
