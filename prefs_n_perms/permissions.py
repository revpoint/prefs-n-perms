from collections import namedtuple, OrderedDict
from prefs_n_perms.base import PrefsNPermsBase
from prefs_n_perms.client import db
from prefs_n_perms.decorators import protect_writable
from prefs_n_perms.settings import preference_settings

PermissionSet = namedtuple('PermissionSet', ['allowed', 'blocked'])


class Permissions(PrefsNPermsBase):
    prefix = preference_settings.PERMISSIONS_PREFIX
    global_tier = 'available'

    def get_db_obj(self, key):
        return db.Set(key)

    def add_global_db_obj(self):
        pass

    def add_tier_db_obj(self, tier, key):
        self.tiers[tier] = PermissionSet(self.get_db_obj(key + ':allowed'),
                                         self.get_db_obj(key + ':blocked'))

    def get_available_perms(self):
        return self.get_global_db_obj()

    @protect_writable
    def add_available_perms(self, *perms):
        available = self.get_available_perms()
        map(available.add, perms)

    @protect_writable
    def remove_available_perms(self, *perms):
        available = self.get_available_perms()
        map(available.remove, perms)

    def get_allowed_perms_for_tier(self, tier):
        return self.tiers[tier].allowed

    def tier_has_allowed_perm(self, tier, name):
        return name in self.get_allowed_perms_for_tier(tier)

    @protect_writable
    def add_allowed_perms_to_tier(self, tier, *perms):
        allowed = self.get_allowed_perms_for_tier(tier)
        map(allowed.add, perms)

    @protect_writable
    def remove_allowed_perms_from_tier(self, tier, *perms):
        allowed = self.get_allowed_perms_for_tier(tier)
        map(allowed.remove, perms)

    def get_blocked_perms_for_tier(self, tier):
        return self.tiers[tier].blocked

    def tier_has_blocked_perm(self, tier, name):
        return name in self.get_blocked_perms_for_tier(tier)

    @protect_writable
    def add_blocked_perms_to_tier(self, tier, *perms):
        blocked = self.get_blocked_perms_for_tier(tier)
        map(blocked.add, perms)

    @protect_writable
    def remove_blocked_perms_from_tier(self, tier, *perms):
        blocked = self.get_blocked_perms_for_tier(tier)
        map(blocked.remove, perms)

    def get_perms(self):
        perms = PermissionSet(set(), set())
        for tier in self.tiers.itervalues():
            perms.allowed.update(tier.allowed)
            perms.blocked.update(tier.blocked)
        return perms.allowed - perms.blocked

    def has_perm(self, name):
        return name in self.get_perms()

    @protect_writable
    def add_perms(self, *perms):
        self.add_allowed_perms_to_tier(self.last_tier, *perms)

    @protect_writable
    def remove_perms(self, *perms):
        self.remove_allowed_perms_from_tier(self.last_tier, *perms)

    def get_all_tiers(self):
        perms = OrderedDict()
        for tier, (allowed, blocked) in self.tiers.iteritems():
            perms[tier] = {
                'allowed': set(allowed),
                'blocked': set(blocked),
            }
        return perms
