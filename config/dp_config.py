import datetime
import redis.asyncio as redis
from redis.exceptions import ConnectionError
from config.bot_config import tgpt
from aiogram import Dispatcher, F
from aiogram.fsm.storage.redis import RedisStorage


# the idea is to use redis ttl cache in order to prevent long caching of unused data
redis_pool = redis.ConnectionPool(host="127.0.0.1",
                                  port=6379,
                                  socket_timeout=1)
redis_client = redis.client.Redis(connection_pool=redis_pool)

try:
    await redis_client.ping()
    session_rate_limit = datetime.timedelta(minutes=10)
    storage = RedisStorage(
        redis=redis_client,
        state_ttl=session_rate_limit,
        data_ttl=session_rate_limit
    )
except ConnectionError:
    from aiogram.fsm.storage.memory import MemoryStorage
    storage = MemoryStorage()

dp = Dispatcher(bot=tgpt, storage=storage)
dp.message.filter(F.chat.type == "private")

