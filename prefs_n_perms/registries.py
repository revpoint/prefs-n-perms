from collections import defaultdict
import inspect
from django.conf import settings
from importlib import import_module
from prefs_n_perms.config import SectionConfig, ModelConfig
from prefs_n_perms.exceptions import SectionAlreadyRegisteredException, SectionNotRegisteredException, \
    TierAlreadyRegisteredException
from prefs_n_perms.sections import Section
from prefs_n_perms.settings import preference_settings


class SectionRegistry(dict):
    def register(self, section, config):
        if not issubclass(config, SectionConfig) or not inspect.isclass(config):
            raise ValueError
        if section in self:
            raise SectionAlreadyRegisteredException

        config = config(section)
        self[section] = config

        return config

    def unregister(self, section):
        del self[section]


class ModelRegistry(defaultdict):
    def __init__(self, **kwargs):
        super(ModelRegistry, self).__init__(dict, **kwargs)

    def register(self, section, tier, config):
        if not issubclass(config, ModelConfig) or not inspect.isclass(config):
            raise ValueError
        if section not in section_registry:
            raise SectionNotRegisteredException
        if tier in self[section]:
            raise TierAlreadyRegisteredException

        section_config = section_registry[section]
        config = config(section_config, tier)
        self[section][tier] = config

        return config

    def unregister(self, section, tier):
        del self[section][tier]


def autodiscover():
    """
    Populate the registry by iterating through every section declared in :py:const:`settings.INSTALLED_APPS`.
    """
    for app in settings.INSTALLED_APPS:
        package = '{0}.{1}'.format(app, preference_settings.REGISTRY_MODULE)
        try:
            import_module(package)
        except ImportError:
            pass


section_registry = SectionRegistry()
model_registry = ModelRegistry()
