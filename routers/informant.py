from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


informant = Router()

@informant.message(Command('help'))
async def help(message: Message) -> None:
    return await message.answer("""
Данный бот создан для того, чтобы помочь вам утилизировать силу LLM на максимум.
Конечная цель проекта - предложить пользователи всевозможные инструменты для решения повседневных задач.
# TODO #
""")
