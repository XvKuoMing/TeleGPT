from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


informant = Router()

@informant.message(Command('donate'))
async def ask_to_donate(message: Message) -> None:
    await message.answer(text="""
    На данный момент сервис работает на raspberry pi 3B+. 
    Его хватает для работы бота, но не для добавления новых бесплатных фичей.
    Если вам нравится проект и вы хотите его продолжение, то мы открыты к любому донату:
    Сбер: 5469 3800 6031 5628 
    """)
