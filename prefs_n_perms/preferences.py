from collections import OrderedDict
from prefs_n_perms.base import PrefsNPermsBase
from prefs_n_perms.client import db
from prefs_n_perms.decorators import protect_writable, cached_property
from prefs_n_perms.settings import preference_settings


class Preferences(PrefsNPermsBase):
    prefix = preference_settings.PREFERENCES_PREFIX
    cached_objects = ('all_prefs',)

    def get_db_obj(self, key):
        return db.Dict(key)

    def get_prefs_for(self, tier):
        return self.tiers[tier]

    def get_pref_for(self, tier, name):
        return self.get_prefs_for(tier).get(name)

    @protect_writable
    def set_prefs_for(self, tier, new_prefs):
        prefs = self.get_prefs_for(tier)
        prefs.update(new_prefs)

    @protect_writable
    def set_pref_for(self, tier, name, value):
        prefs = self.get_prefs_for(tier)
        prefs[name] = value

    @protect_writable
    def remove_prefs_for(self, tier, *name):
        prefs = self.get_prefs_for(tier)
        prefs.client.hdel(prefs.name, *name)

    def set_global_prefs(self, new_prefs):
        self.set_prefs_for(self.global_tier, new_prefs)

    def set_global_pref(self, name, value):
        self.set_pref_for(self.global_tier, name, value)

    def remove_global_prefs(self, *name):
        self.remove_prefs_for(self.global_tier, *name)

    def set_prefs(self, new_prefs):
        self.set_prefs_for(self.last_tier, new_prefs)

    def set_pref(self, name, value):
        self.set_pref_for(self.last_tier, name, value)

    def remove_prefs(self, *name):
        self.remove_prefs_for(self.last_tier, *name)

    def get_prefs(self):
        prefs = {}
        for tier in self.tiers.itervalues():
            prefs.update(tier)
        return prefs
    all_prefs = cached_property(get_prefs, name='all_prefs')

    def get_pref(self, name):
        pref = None
        for tier in self.tiers.itervalues():
            pref = tier.get(name, pref)
        return pref

    def get_all_tiers(self):
        prefs = OrderedDict()
        for tier, db_obj in self.tiers.iteritems():
            prefs[tier] = dict(db_obj)
        return prefs
