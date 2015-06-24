from collections import OrderedDict
import collections
from prefs_n_perms.base import PrefsNPermsBase
from prefs_n_perms.client import db
from prefs_n_perms.decorators import protect_writable, cached_property
from prefs_n_perms.settings import preference_settings


class Preferences(PrefsNPermsBase, collections.MutableMapping):
    prefix = preference_settings.PREFERENCES_PREFIX

    def __repr__(self):
        return repr(self.all)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        return self.set(key, value)

    def __delitem__(self, key):
        return self.remove(key)

    def __iter__(self):
        return iter(self.all.keys())

    def __len__(self):
        return len(self.all)

    def get_db_obj(self, key):
        return db.Dict(key)

    def get_for(self, tier, name):
        return self.get_tier(tier).get(name)

    @protect_writable
    def update_tier(self, tier, new_prefs):
        prefs = self.get_tier(tier)
        prefs.update(new_prefs)

    @protect_writable
    def set_for(self, tier, name, value):
        prefs = self.get_tier(tier)
        prefs[name] = value

    @protect_writable
    def remove_for(self, tier, *name):
        prefs = self.get_tier(tier)
        prefs.client.hdel(prefs.name, *name)

    def update_global(self, new_prefs):
        self.update_tier(self.global_tier, new_prefs)

    def set_global(self, name, value):
        self.set_for(self.global_tier, name, value)

    def remove_global(self, *name):
        self.remove_for(self.global_tier, *name)

    def update(*args, **kwargs):
        if len(args) > 2:
            raise TypeError("update() takes at most 2 positional "
                            "arguments ({} given)".format(len(args)))
        elif not args:
            raise TypeError("update() takes at least 1 argument (0 given)")
        self = args[0]
        other = {}
        other.update(args[1] if len(args) >= 2 else {})
        other.update(kwargs)
        self.update_tier(self.last_tier, other)

    def set(self, name, value):
        self.set_for(self.last_tier, name, value)

    def remove(self, *name):
        self.remove_for(self.last_tier, *name)

    @cached_property
    def all(self):
        prefs = {}
        for tier in self.tiers.itervalues():
            prefs.update(tier)
        return prefs

    def get(self, name, default=None):
        pref = default
        for tier in self.tiers.itervalues():
            pref = tier.get(name, pref)
        return pref

    def all_tiers(self):
        prefs = OrderedDict()
        for tier, db_obj in self.tiers.iteritems():
            prefs[tier] = dict(db_obj)
        return prefs
