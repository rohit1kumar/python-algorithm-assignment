import json
from redis import Redis
from typing import Optional


class CacheService:
    def __init__(self, host: str = "127.0.0.1", port: int = 6379):
        self.redis = Redis(host=host, port=port, decode_responses=True)
        self.expiry = 3600  # 1 hour cache expiry

    def get_key(self, prefix: str, data: dict) -> str:
        """Generate a cache key from prefix and input data"""
        sorted_data = json.dumps(data, sort_keys=True)
        return f"{prefix}:{sorted_data}"

    def get(self, key: str) -> Optional[str]:
        """Get value from cache"""
        return self.redis.get(key)

    def set(self, key: str, value: str) -> None:
        """Set value in cache with expiry"""
        self.redis.set(key, value, ex=self.expiry)
