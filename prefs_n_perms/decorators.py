from functools import wraps
from prefs_n_perms.exceptions import ReadOnlyException


def protect_writable(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.read_only:
            raise ReadOnlyException
        return f(self, *args, **kwargs)
    return wrapper
