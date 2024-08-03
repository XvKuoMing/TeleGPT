from aiogram import F, Router, flags
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.storage.base import StorageKey

from config.bot_config import bot
from config.dp_config import dp
from utils.generation import generate_answer

generator = Router()


@generator.message(~F.text.startswith('/') & F.text)
@flags.chat_action(initial_sleep=1, action="typing", interval=3)
async def proceed_dialog(message: Message) -> None:
    storage_key = StorageKey(bot_id=bot.id,
                             user_id=message.from_user.id,
                             chat_id=message.chat.id)
    data = await dp.storage.get_data(key=storage_key)
    history = []
    if 'history' in data.keys():
        history = data['history']
    ai_answer = await message.answer(
                    text=await generate_answer(
                        prompt=message.text,
                        history=history
                    )
                )
    history.append({'role': 'user', 'content': message.text})
    history.append({'role': 'assistant', 'content': ai_answer.text})
    await dp.storage.update_data(key=storage_key,
                                 data={'history': history})


@generator.message(Command('clear'))
async def clear_chat_history(message: Message) -> None:
    storage_key = StorageKey(bot_id=bot.id,
                             user_id=message.from_user.id,
                             chat_id=message.chat.id)
    await dp.storage.update_data(key=storage_key, data={'history': []})
    await message.answer(text='История сообщений очищена')
