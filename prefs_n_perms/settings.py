# Taken from django-rest-framework
# https://github.com/tomchristie/django-rest-framework
# Copyright (c) 2011-2015, Tom Christie All rights reserved.

from __future__ import unicode_literals
import os
from django.test.signals import setting_changed
from django.utils import six
import importlib

SETTINGS_ATTR = 'PREFS_N_PERMS'

# Only pull Django settings if Django environment variable exists.
if os.environ.get('DJANGO_SETTINGS_MODULE'):
    from django.conf import settings
    USER_SETTINGS = getattr(settings, SETTINGS_ATTR, None)
else:
    USER_SETTINGS = None


DEFAULTS = {
    'REDIS_URL': 'redis://localhost:6379/0',
    'REGISTRY_MODULE': 'prefs_n_perms',
    'SECTIONS_PREFIX': 'sections',
    'PREFERENCES_PREFIX': 'preferences',
    'PERMISSIONS_PREFIX': 'permissions',
}


# List of settings that may be in string import notation.
IMPORT_STRINGS = (

)


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, six.string_types):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        # Nod to tastypie's use of importlib.
        parts = val.split('.')
        module_path, class_name = '.'.join(parts[:-1]), parts[-1]
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except ImportError as e:
        msg = "Could not import '%s' for API setting '%s'. %s: %s." % (val, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)


class PreferenceSettings(object):
    """
    A settings object, that allows API settings to be accessed as properties.
    For example:

        from rest_framework.settings import api_settings
        print(api_settings.DEFAULT_RENDERER_CLASSES)

    Any setting with string import paths will be automatically resolved
    and return the class, rather than the string literal.
    """
    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        self.user_settings = user_settings or {}
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS

    def __getattr__(self, attr):
        if attr not in self.defaults.keys():
            raise AttributeError("Invalid preference setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if val and attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        setattr(self, attr, val)
        return val


preference_settings = PreferenceSettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)


def reload_prefs_settings(*args, **kwargs):
    global preference_settings
    setting, value = kwargs['setting'], kwargs['value']
    if setting == SETTINGS_ATTR:
        preference_settings = PreferenceSettings(value, DEFAULTS, IMPORT_STRINGS)


setting_changed.connect(reload_prefs_settings)
