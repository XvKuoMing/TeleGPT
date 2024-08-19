from aiogram import Bot
import os
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
load_dotenv()

tgpt = Bot(
    token=os.getenv('BOT_TOKEN'),
    default=DefaultBotProperties(parse_mode="MarkdownV2")
)
