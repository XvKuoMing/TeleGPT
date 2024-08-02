import asyncio
import logging
from aiogram import F, flags
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionMiddleware

from config.bot_config import bot
from config.dp_config import dp
from utils.generation import generate_answer
from routers.generator import generator

@dp.message(Command('start'))
@flags.chat_action(initial_sleep=1, action="typing", interval=3)
async def start_session(message: Message) -> None:
    name = message.from_user.full_name
    text = await generate_answer(
        prompt='Поприветствуй пользователя с именем {name}. Расскажи ему пару слов о себе и что ты умеешь.'
    )
    text = text.format(name=name)
    await message.answer(text=text)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.message.middleware(ChatActionMiddleware())
    generator.message.middleware(ChatActionMiddleware())

    dp.include_router(generator)
    await dp.start_polling(bot)


logging.basicConfig(
    filename="info.log",
    filemode='a',
    level=logging.INFO
)
# updating docker container https://www.quora.com/How-do-you-update-code-in-a-docker-container
# https://docs.docker.com/build/ci/
asyncio.run(main())
