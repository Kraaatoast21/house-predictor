import functools
import time

class SystemCache:
    def __init__(self):
        self._cache = {}
        self._expiry = {}

    def memoize(self, ttl=300):
        """
        Cache decorator with Time-To-Live (TTL) in seconds.
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = (func.__name__, args, frozenset(kwargs.items()))
                
                # Check if exists and not expired
                if key in self._cache:
                    if time.time() < self._expiry.get(key, 0):
                        return self._cache[key]
                
                # Execute and cache
                result = func(*args, **kwargs)
                self._cache[key] = result
                self._expiry[key] = time.time() + ttl
                return result
            
            # Allow manual clearing
            def clear_this():
                keys_to_del = [k for k in self._cache.keys() if k[0] == func.__name__]
                for k in keys_to_del:
                    self._cache.pop(k, None)
                    self._expiry.pop(k, None)
            
            wrapper.invalidate = clear_this
            return wrapper
        return decorator

    def clear_all(self):
        """Reset the entire cache."""
        self._cache.clear()
        self._expiry.clear()

# Global singleton for application-wide caching
GLOBAL_CACHE = SystemCache()
