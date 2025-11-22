import time
from typing import Any, Dict, Optional

class Cache:
    def __init__(self, default_ttl: int = 300):
        self.default_ttl = default_ttl
        self._cache: Dict[str, tuple[float, Any]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            expiry_time, value = self._cache[key]
            if time.time() < expiry_time:
                return value
            else:
                del self._cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        expiry_time = time.time() + (ttl or self.default_ttl)
        self._cache[key] = (expiry_time, value)
    
    def clear(self):
        self._cache.clear()