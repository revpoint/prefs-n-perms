from importlib import import_module

from prefs_n_perms.exceptions import PrefsNPermsException


def load_class(path):
    """
    Loads class from path.
    """

    mod_name, klass_name = path.rsplit('.', 1)

    try:
        mod = import_module(mod_name)
    except AttributeError as e:
        raise PrefsNPermsException('Error importing {0}: "{1}"'.format(mod_name, e))

    try:
        klass = getattr(mod, klass_name)
    except AttributeError:
        raise PrefsNPermsException('Module "{0}" does not define a "{1}" class'.format(mod_name, klass_name))

    return klass
