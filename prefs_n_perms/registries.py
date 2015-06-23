from django.conf import settings
from django.utils.importlib import import_module
from prefs_n_perms.settings import preference_settings


class SectionRegistry(dict):
    def register(self, section, model):
        return model


class PreferencesRegistry(dict):
    def register(self, section, model):
        return model


class PermissionsRegistry(dict):
    def register(self, section, model):
        return model


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
preferences_registry = SectionRegistry()
permissions_registry = SectionRegistry()
