from __future__ import unicode_literals

import django
from django.core.cache.backends import locmem

from caching.compat import DEFAULT_TIMEOUT, FOREVER


if django.VERSION[:2] >= (1, 6):
    Infinity = FOREVER
else:
    class _Infinity(object):
        """Always compares greater than numbers."""

        def __radd__(self, _):
            return self

        def __cmp__(self, o):
            return 0 if self is o else 1

        def __repr__(self):
            return 'Infinity'

    Infinity = _Infinity()
    del _Infinity


# Add infinite timeout support to the locmem backend.  Useful for testing.
class InfinityMixin(object):

    def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        if timeout == FOREVER:
            timeout = Infinity
        return super(InfinityMixin, self).add(key, value, timeout, version)

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        if timeout == FOREVER:
            timeout = Infinity
        return super(InfinityMixin, self).set(key, value, timeout, version)


class LocMemCache(InfinityMixin, locmem.LocMemCache):
    pass
