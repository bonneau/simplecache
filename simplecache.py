import time

from collections import OrderedDict
from threading import Condition


class SimpleCache(object):
    def __init__(self, timeout=None, max_items=1000):
        if max_items is None or max_items <= 0:
            raise Exception("max_items must be a positive integer")

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

    def __iter__(self):
        # TODO: Implement
        pass

    def __expire_if_necessary(self, k, t):
        if t and time.time() > t:
            del self._d[k]
            raise KeyError(k)

    def __prune_if_necessary(self):
        if len(self._d) > self._max_items:
            self._d.popitem(last=False)


class ThreadSafeSimpleCache(SimpleCache):
    def __init__(self):
        super(ThreadSafeSimpleCache, self).__init__()
        self._c = Condition()

    def __len__(self):
        self._c.acquire()
        try:
            return SimpleCache.__len__(self)
        finally:
            self._c.release()

    def __contains__(self, k):
        self._c.acquire()
        try:
            return SimpleCache.__contains__(self, k)
        finally:
            self._c.release()

    def __getitem__(self, k):
        self._c.acquire()
        try:
            return SimpleCache.__getitem__(self, k)
        finally:
            self._c.release()

    def __setitem__(self, k, v):
        self._c.acquire()
        try:
            SimpleCache.__setitem__(self, k, v)
        finally:
            self._c.release()

    def __delitem__(self, k):
        self._c.acquire()
        try:
            SimpleCache.__delitem__(self, k)
        finally:
            self._c.release()

    def __iter__(self):
        self._c.acquire()
        try:
            return SimpleCache.__iter__(self)
        finally:
            self._c.release()
