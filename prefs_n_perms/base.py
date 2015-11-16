from collections import OrderedDict
from prefs_n_perms.client import db
from prefs_n_perms.decorators import protect_writable
from prefs_n_perms.exceptions import ExtraInstancesException, MissingInstancesException, GlobalVariableException
from prefs_n_perms.settings import preference_settings


class PrefsNPermsBase(object):
    prefix = preference_settings.BASE_PREFIX
    global_tier = 'global'
    cached_objects = ('all',)

    def __init__(self, section, require_all=False, read_only=False, **kwargs):
        self.section = section
        self.require_all = require_all
        self.read_only = read_only
        self.instance_keys = self.get_instance_keys(kwargs)
        self.tiers = OrderedDict()
        self.add_tiers()

    def key_for(self, entity):
        return ':'.join((self.prefix, self.section.name, entity))

    def get_instance_keys(self, kwargs):
        """
        Loop through (tier, id) in kwargs, check if ID is a number
        and return a dict((tier, db_key), ...)
        """
        return (dict((k, self.key_for('.'.join((k, str(v)))))
                     for k, v in kwargs.iteritems()
                     if str(v).isdigit())
                if kwargs else {})

    @property
    def global_key(self):
        return self.key_for(self.global_tier)

    def exists(self):
        return self.global_key in db

    def clear_cache(self):
        for obj in self.cached_objects:
            if hasattr(self, obj):
                delattr(self, obj)

    def add_tiers(self):
        self.add_global_db_obj()
        self.validate()

        instance_tiers = self.instance_keys.keys()
        missing_tiers = []

        for tier in self.section.tiers:
            if tier in self.instance_keys:
                self.add_tier_db_obj(tier, self.instance_keys[tier])
                instance_tiers.remove(tier)
            elif len(instance_tiers):
                missing_tiers.append(tier)
            else:
                break

        if missing_tiers:
            raise MissingInstancesException(missing_tiers)

    def validate(self):
        section_tiers = set(self.section.tiers)
        instance_tiers = set(self.instance_keys)

        # If tiers that are not in the section are in the instance keys, raise exception
        if instance_tiers > section_tiers:
            raise ExtraInstancesException(instance_tiers - section_tiers)

        # If require_all is true and instance_tiers does not contain all section_tiers, raise exception
        if self.require_all and instance_tiers < section_tiers:
            raise MissingInstancesException(section_tiers - instance_tiers)

    def get_db_obj(self, key):
        return db.get(key)

    def get_global_db_obj(self):
        return self.get_db_obj(self.global_key)

    def add_global_db_obj(self):
        self.tiers[self.global_tier] = self.get_global_db_obj()

    def add_tier_db_obj(self, tier, key):
        self.tiers[tier] = self.get_db_obj(key)

    @property
    def last_tier(self):
        tier = self.tiers.keys()[-1]
        if tier == self.global_tier:
            raise GlobalVariableException
        return tier

    def get_tier(self, tier):
        return self.tiers[tier]

    def get_last_tier(self):
        return self.get_tier(self.last_tier)

    @protect_writable
    def clear(self):
        try:
            prefs = self.get_tier(self.last_tier)
            db.api.delete(prefs.name)
        except KeyError:
            pass
