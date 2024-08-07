from aiogram import F, Router, flags
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.storage.base import StorageKey

from config.bot_config import tgpt
from config.dp_config import dp
from utils.generation import generate_answer
from utils.stt import voice_file_id2text
from typing import Optional

generator = Router()  # handles every logic about text generation


@generator.message(~F.text.startswith('/') & F.text)
@flags.chat_action(initial_sleep=1, action="typing", interval=3)
async def proceed_dialog(message: Message, text: Optional[str] = None) -> None:
    """
    The main generation handler, generates texts, saves dialog history
    :param message: message to reply
    :param text: text to generate from, if not provided message.text is used
    :return: replies to message
    """
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

"""-------------------------------------------special generation cases-------------------------------------------"""
@generator.message(Command('start'))
@flags.chat_action(initial_sleep=1, action="typing", interval=3)
async def start_session(message: Message) -> None:
    """
    generate greeting message from manually provided prompt
    :param message:
    :return: replies to user with generated message
    """
    name = message.from_user.full_name
    text = f"""Поприветствуй пользователя с именем {name}. 
    Расскажи ему пару слов о себе и что ты умеешь. 
    Если ты его уже приветствовал, то спроси, чем ему помочь."""
    await proceed_dialog(message=message, text=text)

@generator.message(F.voice)
@flags.chat_action(initial_sleep=1, action="typing", interval=3)
async def voice2text(message: Message) -> None:
    """
    recognises text from voice message and generates text based on the text
    :param message: message that contains voice message
    :return: replies to user with generated text
    """
    voice_file_id = message.voice.file_id
    text = await voice_file_id2text(voice_file_id)
    await proceed_dialog(message=message, text=text)


"""-------------------------------------memory management----------------------------------------------"""
@generator.message(Command('clear'))
async def clear_chat_history(message: Message) -> None:
    """
    allowing user to manually clear dialog history
    :param message: message from user that implies need of history clearing
    :return: success message to user
    """
    storage_key = StorageKey(bot_id=tgpt.id,
                             user_id=message.from_user.id,
                             chat_id=message.chat.id)
    await dp.storage.update_data(key=storage_key, data={'history': []})
    await message.answer(text='История сообщений очищена')
