from dnevnik.util import *
from typing import *

K = TypeVar("K")
V = TypeVar("V")


class Cache(Generic[K, V]):

    def __init__(self, expire_time: float, auto_cleanup: bool = True):
        self.expire_time = expire_time * 1000
        self.auto_cleanup = auto_cleanup

        self.data = dict()
        self.times = dict()

    def cleanup(self):
        for (key, timestamp) in self.times:
            if timestamp + self.expire_time < millis():
                self.remove(key)

    def __auto_cleanup(self):
        if self.auto_cleanup:
            self.cleanup()

    def is_present(self, key) -> bool:
        return self.data.get(key) is not None \
               and self.times.get(key) is not None \
               and self.times.get(key) + self.expire_time > millis()

    def get(self, key) -> V | None:
        self.__auto_cleanup()

        return self.data.get(key) if self.is_present(key) else None

    def set(self, key, value: V):
        self.data[key] = value
        self.times[key] = millis()

    def remove(self, key):
        del self.data[key]
        del self.times[key]

    def clear(self):
        self.data.clear()
        self.times.clear()

    def __setitem__(self, key, value):
        self.set(key, value)

    def __getitem__(self, item):
        return self.get(item)

    def __delitem__(self, key):
        self.remove(key)