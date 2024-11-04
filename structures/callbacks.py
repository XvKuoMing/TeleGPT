from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List


class CallbackChoice(CallbackData, prefix="ch"):
    type: str
    choice: str
    user_id: int


async def choice_callback(type: str, choices: List[str], user_id: int):
    builder = InlineKeyboardBuilder()
    for choice in choices:
        builder.button(
            text=choice,
            callback_data=CallbackChoice(type=type, choice=choice, user_id=user_id)
        )
    builder.adjust(1)
    return builder.as_markup()