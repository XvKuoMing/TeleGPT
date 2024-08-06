from aiogram import Bot
from aiogram.enums import ParseMode
import os
from dotenv import load_dotenv
load_dotenv()

tgpt = Bot(
    token=os.getenv('BOT_TOKEN'),
    # parse_mode=ParseMode.HTML
)
