from aiogram import Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage

from config.bot_config import bot

storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
dp.message.filter(F.chat.type == "private")