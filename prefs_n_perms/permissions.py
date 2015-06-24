from collections import namedtuple, OrderedDict
from prefs_n_perms.base import PrefsNPermsBase
from prefs_n_perms.client import db
from prefs_n_perms.decorators import protect_writable, cached_property
from prefs_n_perms.settings import preference_settings

PermissionSet = namedtuple('PermissionSet', ['allowed', 'blocked'])


class Permissions(PrefsNPermsBase):
    prefix = preference_settings.PERMISSIONS_PREFIX
    global_tier = 'available'
    cached_objects = ('all_perms',)

    def get_db_obj(self, key):
        return db.Set(key)

    def add_global_db_obj(self):
        pass

    def add_tier_db_obj(self, tier, key):
        self.tiers[tier] = PermissionSet(self.get_db_obj(key + ':allowed'),
                                         self.get_db_obj(key + ':blocked'))

    @property
    def available(self):
        return self.get_global_db_obj()

    @protect_writable
    def add_available(self, *perms):
        map(self.available.add, perms)

    @protect_writable
    def remove_available_perms(self, *perms):
        map(self.available.remove, perms)

    def get_allowed_for(self, tier):
        return self.tiers[tier].allowed

    def tier_is_allowed(self, tier, name):
        return name in self.get_allowed_for(tier)

    @protect_writable
    def add_allowed_for(self, tier, *perms):
        allowed = self.get_allowed_for(tier)
        map(allowed.add, perms)

    @protect_writable
    def remove_allowed_for(self, tier, *perms):
        allowed = self.get_allowed_for(tier)
        map(allowed.remove, perms)

    def get_blocked_for(self, tier):
        return self.tiers[tier].blocked

    def tier_is_blocked(self, tier, name):
        return name in self.get_blocked_for(tier)

    @protect_writable
    def add_blocked_for(self, tier, *perms):
        blocked = self.get_blocked_for(tier)
        map(blocked.add, perms)

    @protect_writable
    def remove_blocked_for(self, tier, *perms):
        blocked = self.get_blocked_for(tier)
        map(blocked.remove, perms)

    def add_perms(self, *perms):
        self.add_allowed_for(self.last_tier, *perms)

    def remove_perms(self, *perms):
        self.remove_allowed_for(self.last_tier, *perms)

    def block_perms(self, *perms):
        self.add_blocked_for(self.last_tier, *perms)

    def unblock_perms(self, *perms):
        self.remove_blocked_for(self.last_tier, *perms)

    def get_perms(self):
        perms = PermissionSet(set(), set())
        for tier in self.tiers.itervalues():
            perms.allowed.update(tier.allowed)
            perms.blocked.update(tier.blocked)
        return perms.allowed - perms.blocked
    all_perms = cached_property(get_perms, name='all_perms')

    def has_perm(self, name):
        return name in self.all_perms

    def get_all_tiers(self):
        perms = OrderedDict()
        for tier, (allowed, blocked) in self.tiers.iteritems():
            perms[tier] = {
                'allowed': set(allowed),
                'blocked': set(blocked),
            }
        return perms
