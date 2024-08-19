import datetime
import redis
import redis.asyncio as aioredis
from redis.exceptions import ConnectionError
from config.bot_config import tgpt
from aiogram import Dispatcher, F
from aiogram.fsm.storage.redis import RedisStorage


try:
    redis_host_params = {
        "host": "127.0.0.1",
        "port": 6379,
        "socket_timeout": 1,
    }
    # test connection
    conn = redis.client.Redis(**redis_host_params)
    conn.ping()
    conn.close()
    # production connection
    redis_pool = aioredis.ConnectionPool(**redis_host_params)
    redis_client = aioredis.client.Redis(connection_pool=redis_pool)
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

