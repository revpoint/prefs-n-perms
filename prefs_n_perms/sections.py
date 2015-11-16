from prefs_n_perms.client import db
from prefs_n_perms.permissions import Permissions
from prefs_n_perms.preferences import Preferences
from prefs_n_perms.settings import preference_settings


class Section(object):
    prefix = preference_settings.SECTIONS_PREFIX

    def __init__(self, name, **kwargs):
        self.name = name

    def __str__(self):
        return self.name

    @property
    def section_key(self):
        return ':'.join((self.prefix, self.name))

    def exists(self):
        return self.section_key in db

    @property
    def has_preferences(self):
        return Preferences(self).exists()

    @property
    def has_permissions(self):
        return Permissions(self).exists()

    def get_preferences(self, **kwargs):
        return Preferences(self, **kwargs)

    def get_permissions(self, **kwargs):
        return Permissions(self, **kwargs)

    @property
    def tiers(self):
        return db.List(self.section_key)

    @tiers.setter
    def tiers(self, value):
        if not isinstance(value, (tuple, list)):
            raise ValueError
        if self.exists():
            db.api.delete(self.section_key)
        db.List(self.section_key, value)
