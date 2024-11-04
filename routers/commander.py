'''роутер для выполнения команд, связанных с конфигурацией бота'''
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from structures.callbacks import choice_callback, CallbackChoice
from aiogram.fsm.storage.base import StorageKey
from config.dp_config import dp
from config.bot_config import tgpt
from config.openai_config import SYSTEM_PROMPTS
from routers.generator import proceed_dialog


commander = Router()


DO = "do"

@commander.message(Command(DO))
async def change_bot_system(message: Message) -> None:
    """Change system prompt for current user"""
    await message.answer(
        "Пожалуйста, выберите, что вы хотите сделать?",
        reply_markup=await choice_callback(
            type=DO,
            choices=list(SYSTEM_PROMPTS.keys()),
            user_id=message.from_user.id
        )
    )

@commander.callback_query(CallbackChoice.filter(F.type == DO))
async def save_choice(query: CallbackQuery, callback_data: CallbackChoice) -> None:
    await query.answer()
    new_system = SYSTEM_PROMPTS[callback_data.choice]
    storage_key = StorageKey(
        bot_id=tgpt.id,
        user_id=callback_data.user_id,
        chat_id=query.message.chat.id
    )
    await dp.storage.update_data(key=storage_key,
                                    data={'system': new_system})
    await proceed_dialog(
        message=query.message,
        text="Спроси пользователя, чем ему помочь. Расскажи, что ты можешь."
    )
