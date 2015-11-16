from collections import namedtuple, OrderedDict
import collections
from prefs_n_perms.base import PrefsNPermsBase
from prefs_n_perms.client import db
from prefs_n_perms.decorators import protect_writable, cached_property
from prefs_n_perms.settings import preference_settings

PermissionSet = namedtuple('PermissionSet', ['allowed', 'blocked'])


class Permissions(PrefsNPermsBase, collections.MutableSet):
    prefix = preference_settings.PERMISSIONS_PREFIX
    global_tier = 'available'

    def __repr__(self):
        return repr(self.all)

    def __contains__(self, item):
        return item in self.all

    def __iter__(self):
        return iter(self.all)

    def __len__(self):
        return len(self.all)

    def get_db_obj(self, key):
        return db.Set(key)

    def get_global_db_obj(self):
        return db.SortedSet(self.global_key)

    def add_global_db_obj(self):
        pass

    def add_tier_db_obj(self, tier, key):
        self.tiers[tier] = PermissionSet(self.get_db_obj(key + ':allowed'),
                                         self.get_db_obj(key + ':blocked'))

    @protect_writable
    def _add(self, db_obj, *vals):
        if len(vals) == 1 and isinstance(vals[0], (list, tuple, set)):
            vals = list(vals[0])
        db_obj.client.sadd(db_obj.name, *vals)

    @protect_writable
    def _rem(self, db_obj, *vals):
        if len(vals) == 1 and isinstance(vals[0], (list, tuple, set)):
            vals = list(vals[0])
        db_obj.client.srem(db_obj.name, *vals)

    @property
    def all_available(self):
        return self.get_global_db_obj()

    @property
    def available(self):
        blocked = set()
        [blocked.update(b) for tier, (_, b) in self.tiers.iteritems() if tier != self.last_tier]
        return [p for p in self.all_available if p not in blocked]

    def clear_available(self):
        try:
            db.api.delete(self.global_key)
        except KeyError:
            pass

    def update_available(self, perms):
        if perms:
            self.clear_available()
            perms = reduce(tuple.__add__, enumerate(perms))
            db.api.zadd(self.global_key, *perms)

    def get_allowed_for(self, tier):
        return self.get_tier(tier).allowed

    def is_allowed_for(self, tier, name):
        return name in self.get_allowed_for(tier)

    def add_allowed_for(self, tier, *perms):
        allowed = self.get_allowed_for(tier)
        self._add(allowed, *perms)

    def remove_allowed_for(self, tier, *perms):
        allowed = self.get_allowed_for(tier)
        self._rem(allowed, *perms)

    def get_blocked_for(self, tier):
        return self.get_tier(tier).blocked

    def is_blocked_for(self, tier, name):
        return name in self.get_blocked_for(tier)

    def add_blocked_for(self, tier, *perms):
        blocked = self.get_blocked_for(tier)
        self._add(blocked, *perms)

    def remove_blocked_for(self, tier, *perms):
        blocked = self.get_blocked_for(tier)
        self._rem(blocked, *perms)

    def add(self, *perms):
        if perms:
            self.add_allowed_for(self.last_tier, *perms)

    def remove(self, *perms):
        if perms:
            self.remove_allowed_for(self.last_tier, *perms)
    discard = remove

    def block(self, *perms):
        if perms:
            self.add_blocked_for(self.last_tier, *perms)

    def unblock(self, *perms):
        if perms:
            self.remove_blocked_for(self.last_tier, *perms)

    @protect_writable
    def clear(self):
        try:
            tier = self.get_tier(self.last_tier)
            db.api.delete(tier.allowed.name)
            db.api.delete(tier.blocked.name)
        except KeyError:
            pass

    @property
    def all_tiers(self):
        perms = OrderedDict()
        for tier, (allowed, blocked) in self.tiers.iteritems():
            perms[tier] = {
                'allowed': set(allowed),
                'blocked': set(blocked),
            }
        return perms

    @cached_property
    def all(self):
        perms = PermissionSet(set(), set())
        for allowed, blocked in self.tiers.itervalues():
            perms.allowed.update(allowed)
            perms.blocked.update(blocked)
        return perms.allowed - perms.blocked

    @property
    def inherited(self):
        perms = PermissionSet(set(), set())
        for tier, (allowed, blocked) in self.tiers.iteritems():
            if tier != self.last_tier:
                perms.allowed.update(allowed)
                perms.blocked.update(blocked)
        return perms.allowed - perms.blocked

    def has_perm(self, name):
        return name in self.all
