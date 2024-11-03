import datetime
import redis
import time
import redis.asyncio as aioredis
from redis.exceptions import ConnectionError, TimeoutError
from config.bot_config import tgpt
from aiogram import Dispatcher, F
from aiogram.fsm.storage.redis import RedisStorage



redis_host_params = {
    "host": "127.0.0.1",
    "port": 6379,
    "socket_timeout": 5,
}

# Function to test Redis connection with retries
def test_redis_connection(redis_host_params, max_retries=2, wait_time=2):
    for attempt in range(max_retries):
        try:
            # Test connection
            conn = redis.Redis(**redis_host_params)
            conn.ping()  # if Redis does not reply, the error will occur
            conn.close()
            return True  # Connection successful
        except (TimeoutError, ConnectionError):
            print(f"Redis connection attempt {attempt + 1} failed, retrying...")
            time.sleep(wait_time)  # Wait before retrying
    return False  # Failed after max retries



# Attempt to connect to Redis
if test_redis_connection(redis_host_params):
    # Production connection
    redis_pool = aioredis.ConnectionPool(**redis_host_params)
    redis_client = aioredis.client.Redis(connection_pool=redis_pool)
    session_rate_limit = datetime.timedelta(minutes=60)
    storage = RedisStorage(
        redis=redis_client,
        state_ttl=session_rate_limit,
        data_ttl=session_rate_limit
    )
else:
    # Fallback to in-memory storage if Redis is not available
    from aiogram.fsm.storage.memory import MemoryStorage
    print("Failed to connect to redis, fallback to memory-storage")
    storage = MemoryStorage()

# Initialize the Dispatcher
dp = Dispatcher(bot=tgpt, storage=storage)
dp.message.filter(F.chat.type == "private")

