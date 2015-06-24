from functools import wraps
from prefs_n_perms.exceptions import ReadOnlyException


def protect_writable(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.read_only:
            raise ReadOnlyException
        ret = f(self, *args, **kwargs)
        self.clear_cache()
        return ret
    return wrapper


class cached_property(object):
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance.

    Optional ``name`` argument allows you to make cached properties of other
    methods. (e.g.  url = cached_property(get_absolute_url, name='url') )
    """
    def __init__(self, func, name=None):
        self.func = func
        self.__doc__ = getattr(func, '__doc__')
        self.name = name or func.__name__

    def __get__(self, instance, type=None):
        if instance is None:
            return self
        res = instance.__dict__[self.name] = self.func(instance)
        return res
