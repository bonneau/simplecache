import time

from collections import OrderedDict
from threading import Condition


class SimpleCache:
    def __init__(self, timeout=None, max_items=None):
        self._c = Condition()
        self._d = OrderedDict()
        self._timeout = timeout
        self._max_items = max_items

    def __len__(self):
        self._c.acquire()
        try:
            return len(self._d)
        finally:
            self._c.release()

    def __contains__(self, k):
        self._c.acquire()
        try:
            if k in self._d:
                v, t = self._d[k]
                self.__expire_if_necessary(k, t)
                return k in self._d
            else:
                return False
        finally:
            self._c.release()

    def __getitem__(self, k):
        self._c.acquire()
        try:
            v, t = self._d[k]
            self.__expire_if_necessary(k, t)

            # Delete and re-add; read reference resets expiration
            del self._d[k]
            self[k] = v

            return v
        finally:
            self._c.release()

    def __setitem__(self, k, v):
        self._c.acquire()
        try:
            timeout = None
            if self._timeout:
                timeout = time.time() + self._timeout
            self._d[k] = (v, timeout)
            self.__prune_if_necessary()
        finally:
            self._c.release()

    def __delitem__(self, k):
        self._c.acquire()
        try:
            del self._d[k]
        finally:
            self._c.release()

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