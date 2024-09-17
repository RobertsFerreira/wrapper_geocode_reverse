import time
from collections import OrderedDict
from typing import Any

from pydantic import BaseModel, Field


class SimpleCache(BaseModel):
    cache: OrderedDict = Field(default=OrderedDict())
    capacity: int = Field(default=100)

    def get(self, key: str) -> Any | None:
        if key not in self.cache:
            return None

        value, expire_at = self.cache.get(key, None)

        if not expire_at or time.time() > expire_at:
            return None

        self.cache.move_to_end(key)

        return value

    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        expire_at = time.time() + ttl
        if key in self.cache:
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = (value, expire_at)

    def remove_expired(self):
        expired_keys = [
            key
            for key, (value, expire_at) in self.cache.items()
            if expire_at <= time.time()
        ]
        for key in expired_keys:
            self.cache.pop(key)

    def clear(self):
        self.cache.clear()
