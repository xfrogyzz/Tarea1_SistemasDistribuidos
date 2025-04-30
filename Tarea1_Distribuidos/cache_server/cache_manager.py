from collections import OrderedDict

class BaseCache:
    def __init__(self, size_limit=20):
        self.store = OrderedDict()
        self.limit = size_limit
        self.hits = 0
        self.misses = 0

    def fetch(self, key):
        if key in self.store:
            self.hits += 1
            return self._on_hit(key)
        else:
            self.misses += 1
            return None

    def insert(self, key, value):
        if key in self.store:
            self._on_duplicate(key)
        elif len(self.store) >= self.limit:
            self._evict()
        self.store[key] = value

    def stats(self):
        return {
            "cache_hits": self.hits,
            "cache_misses": self.misses,
            "cache_tamano": len(self.store)
        }

    def _evict(self):
        removed = self.store.popitem(last=False)
        print(f"[Cache] Expulsado: {removed[0]}")

    def _on_hit(self, key):
        raise NotImplementedError

    def _on_duplicate(self, key):
        pass


class LRUCache(BaseCache):
    def _on_hit(self, key):
        self.store.move_to_end(key)
        return self.store[key]

    def _on_duplicate(self, key):
        self.store.move_to_end(key)


class FIFOCache(BaseCache):
    def _on_hit(self, key):
        return self.store[key]
