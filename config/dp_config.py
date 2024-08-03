import datetime
import redis
from redis.exceptions import ConnectionError
from config.bot_config import bot
from aiogram import Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage


try:
    # the idea is to use redis ttl cache in order to prevent long caching of unused data
    redis_pool = redis.ConnectionPool(host="redis",
                                      port=6379,
                                      socket_timeout=1)  # https://habr.com/ru/companies/sberbank/articles/736464/
    redis_client = redis.asyncio.client.Redis(connection_pool=redis_pool)  # https://redis-py.readthedocs.io/en/stable/connections.html
    session_rate_limit = datetime.timedelta(minutes=10)
    storage = RedisStorage(
        redis=redis_client,
        state_ttl=session_rate_limit,
        data_ttl=session_rate_limit
    )
except ConnectionError:
    storage = MemoryStorage()

dp = Dispatcher(bot=bot, storage=storage)
dp.message.filter(F.chat.type == "private")
