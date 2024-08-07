from redis import Redis

from prolog_backend.config.redis import redis_settings


class MemoryRepository:
    def __init__(self):
        self.sessions = Redis(
            host=redis_settings.HOST,
            port=redis_settings.PORT,
            password=redis_settings.PASSWORD,
            decode_responses=True,
            db=0,
        )
        self.refresh_tokens_blacklist = Redis(
            host=redis_settings.HOST,
            port=redis_settings.PORT,
            password=redis_settings.PASSWORD,
            decode_responses=True,
            db=1,
        )
