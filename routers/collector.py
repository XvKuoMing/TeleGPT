from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, PreCheckoutQuery, ContentType
from config.payment_config import pay
from config.bot_config import tgpt

collector = Router()


@collector.message(Command("pay"))
async def send_user_invoice(message: Message) -> None:
    "we need to check if user does not have subscription yet"
    await pay(message.chat_id)

@collector.pre_checkout_query()
async def pre_checkout_query(q: PreCheckoutQuery):
    await tgpt.answer_pre_checkout_query(q.id, ok=True)

@collector.message(F.content_types == ContentType.SUCCESSFUL_PAYMENT)
async def successfull_payment(message: Message) -> None:
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await message.answer(f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно")
