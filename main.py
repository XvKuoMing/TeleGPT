import asyncio
import logging
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message

from config.bot_config import bot
from config.dp_config import dp
from config.openai_config import generate_answer

@dp.message(Command('start'))
async def start_session(message: Message) -> None:
    name = message.from_user.full_name
    await message.chat.do("typing")
    text = await generate_answer(
        prompt=f'Поприветствуй пользователя с именем {name}. Расскажи ему пару слов о себе и что ты умеешь.'
    )
    await message.answer(text=text)

@dp.message(F.text)
async def proceed_dialog(message: Message) -> None:
    await message.chat.do("typing")
    await message.answer(
        text=await generate_answer(
            prompt=message.text
        )
    )

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


logging.basicConfig(
    filename="info.log",
    filemode='a',
    level=logging.INFO
)
asyncio.run(main())
