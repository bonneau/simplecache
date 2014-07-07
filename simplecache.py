import time

from collections import OrderedDict


class SimpleCache:
    def __init__(self, timeout=None, max_items=None):
        self._d = OrderedDict()
        self._timeout = timeout
        self._max_items = max_items

    def __len__(self):
        return len(self._d)

    def __contains__(self, k):
        if k in self._d:
            v, t = self._d[k]
            self.__expire_if_necessary(k, t)
            return k in self._d
        else:
            return False

    def __getitem__(self, k):
        v, t = self._d[k]
        self.__expire_if_necessary(k, t)

        # Delete and re-add; read reference resets expiration
        del self._d[k]
        self[k] = v

        return v

    def __setitem__(self, k, v):
        timeout = None
        if self._timeout:
            timeout = time.time() + self._timeout
        self._d[k] = (v, timeout)
        self.__prune_if_necessary()

    def __delitem__(self, k):
        del self._d[k]

    def __iter___(self):
        # TODO: Implement
        pass

    def __expire_if_necessary(self, k, t):
        if t and time.time() > t:
            del self._d[k]
            raise KeyError(k)

    def __prune_if_necessary(self):
        if self._max_items and len(self._d) > self._max_items:
            self._d.popitem(last=False)