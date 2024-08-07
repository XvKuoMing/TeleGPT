from aiogram import F, Router, flags
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.storage.base import StorageKey

from config.bot_config import tgpt
from config.dp_config import dp
from utils.generation import generate_answer
from utils.stt import voice_file_id2text
from typing import Optional

generator = Router()


@generator.message(~F.text.startswith('/') & F.text)
@flags.chat_action(initial_sleep=1, action="typing", interval=3)
async def proceed_dialog(message: Message, text: Optional[str] = None) -> None:
    storage_key = StorageKey(bot_id=tgpt.id,
                             user_id=message.from_user.id,
                             chat_id=message.chat.id)
    data = await dp.storage.get_data(key=storage_key)
    history = []
    if 'history' in data.keys():
        history = data['history']
    if text is None:
        text = message.text
    ai_answer = await message.answer(
                    text=await generate_answer(
                        prompt=text,
                        history=history
                    )
                )
    history.append({'role': 'user', 'content': text})
    history.append({'role': 'assistant', 'content': ai_answer.text})
    await dp.storage.update_data(key=storage_key,
                                 data={'history': history})

@generator.message(F.voice)
@flags.chat_action(initial_sleep=1, action="typing", interval=3)
async def voice2text(message: Message) -> None:
    voice_file_id = message.voice.file_id
    text = await voice_file_id2text(voice_file_id)
    await proceed_dialog(message=message, text=text)

@generator.message(Command('clear'))
async def clear_chat_history(message: Message) -> None:
    storage_key = StorageKey(bot_id=tgpt.id,
                             user_id=message.from_user.id,
                             chat_id=message.chat.id)
    await dp.storage.update_data(key=storage_key, data={'history': []})
    await message.answer(text='История сообщений очищена')
