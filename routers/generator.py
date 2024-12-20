import asyncio
from aiogram import F, Router, flags
from aiogram.filters import Command
from aiogram.types import Message, ContentType
from aiogram.fsm.storage.base import StorageKey

from config.bot_config import tgpt
from config.dp_config import dp
from utils.generation import generate, generate_answer
from utils.fetching import fetch_all
from utils.create_doc import as_doc
# from utils.stt import voice_file_id2text
from typing import Optional
import base64
import aiofiles
import io
import tempfile

generator = Router()  # handles every logic about text generation


@generator.message(~F.text.startswith('/') & (F.text | F.photo))
@flags.chat_action(initial_sleep=1, action="typing", interval=3)
async def proceed_dialog(message: Message, 
                         text: Optional[str] = None
                         ) -> None:
    """
    The main generation handler, generates texts, saves dialog history
    :param message: message to reply
    :param text: text to generate from, if not provided message.text is used
    :return: replies to message
    """
    storage_key = StorageKey(bot_id=tgpt.id,
                             user_id=message.from_user.id,
                             chat_id=message.chat.id)

    base64_images = None
    if message.content_type == ContentType.TEXT:
        text = message.text if text is None else text
    if message.content_type == ContentType.PHOTO:
        base64_images = []
        photo = message.photo[-1]
        file = await tgpt.get_file(photo.file_id)
        photo_bytes = io.BytesIO()
        await tgpt.download_file(file.file_path, photo_bytes)
        photo_bytes.seek(0)  # Go to the start of the BytesIO object
        # Encode the photo to base64
        encoded_string = base64.b64encode(photo_bytes.read()).decode('utf-8')
        base64_images.append(encoded_string)
        text = message.caption if text is None else text
    
    if text is None and base64_images:
        text = "Расскажи, что на картинках"
    
    # <urls>
    if message.entities:
        urls = []
        print(message.entities)
        for entity in message.entities:
            if entity.type == "text_link":
                urls.append(entity.url)
            if entity.type == "url":
                urls.append(text[entity.offset:entity.length])
        urls_and_texts = await fetch_all(urls)
        embed_text = "\n\n"
        for url, text in urls_and_texts:
            embed_text += f"Информация из ссылки: {url}\n" + text
        text += embed_text
    # </urls>

    resulted_text = await generate(
                        text=text,
                        storage_key=storage_key,
                        base64_images=base64_images
                    )
    if len(resulted_text) < 4096:
        await message.answer(resulted_text)
    else:
        # send .txt document
        name, _ = await generate_answer(
            prompt=f"Придумай название для текта (2-3 слова): {text[:100]}", 
            system="Отвечай всегда на русском"
            )
        input_file = await as_doc(resulted_text, name)
        await message.answer_document(input_file)


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
    await message.answer(text="Генерация по аудио пока не поддерживается.\nСобираем деньги на новый сервер")
    # voice_file_id = message.voice.file_id
    # text = await voice_file_id2text(voice_file_id)
    # await proceed_dialog(message=message, text=text)


@generator.message(F.document)
@flags.chat_action(initial_sleep=1, action="typing", interval=3)
async def doc2text(message: Message) -> None:
    async def create_tempfile():
        # Create a temporary file in a separate thread
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, 
                                          lambda: tempfile.NamedTemporaryFile(mode='wb+', delete=True)
                                          )
    # Check if the document is a .txt file
    if message.document.mime_type == 'text/plain':
        file_id = message.document.file_id
        file = await tgpt.get_file(file_id)
        temp_file = await create_tempfile()
        await tgpt.download_file(file.file_path, temp_file)
        temp_file.seek(0)
        async with aiofiles.open(temp_file.name, "r", encoding="utf-8") as f:
            content = await f.read()
        temp_file.close()

        # Send the contents back to the user
        caption = ""
        if message.caption:
            caption = message.caption + f"\n\n Контент файла/документа: <document>\n{message.document.file_name}\n</document>"
        text = caption + content
        
    else:
        text = "На данный момент поддерживаются только файлы формата .txt"
    
    await proceed_dialog(message, text)


"""-------------------------------------generation memory management----------------------------------------------"""
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
