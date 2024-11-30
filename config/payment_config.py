from aiogram.types import LabeledPrice
from config.bot_config import tgpt
import os
from dotenv import load_dotenv
load_dotenv()

PAYMENT_PROVIDER_TOKEN = os.getenv("PAYMENT_PROVIDER_TOKEN")

RUBLE = 100

# PRICES = {
#     "Pro": LabeledPrice(label="Pro подписка", amount=500*RUBLE),
#     "Ultimate": LabeledPrice(label="Ultimate подписка", amount=900*RUBLE)
# }
PRICES = [
    LabeledPrice(label="Pro подписка", amount=500*RUBLE),
    LabeledPrice(label="Ultimate подписка", amount=900*RUBLE)
]

async def pay(chat_id: int) -> None:
    await tgpt.send_invoice(
        chat_id=chat_id,
        title="Подписка на бота",
        description="Активация подписки на бота на 1 месяц",
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency="rub",
        is_flexible=False,
        prices=PRICES,
        start_parameter="one-month-subscription",
        payload="invoice-payload"
    )