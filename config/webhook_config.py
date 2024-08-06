from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from config.bot_config import bot
from config.dp_config import dp
from dotenv import load_dotenv
import os
load_dotenv()  # load .env vars

WEBHOOK_ADDRESS = os.getenv("WEBHOOK_ADDRESS")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")
SERVER_ADDRESS = os.getenv("SERVER_ADDRESS")
SERVER_PORT = os.getenv("SERVER_PORT")
SELF_SIGNED_CERTIFICATE = os.getenv("SELF_SIGNED_CERTIFICATE")

webhook_handler = SimpleRequestHandler(dispatcher=dp,
                                       bot=bot)

async def set_webhook(_bot: Bot):
    await _bot.set_webhook(f"{WEBHOOK_ADDRESS}{WEBHOOK_PATH}",
                           certificate=FSInputFile(SELF_SIGNED_CERTIFICATE))

