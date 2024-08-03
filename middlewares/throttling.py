from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, throttle_time: int = 5):
        self.caches = TTLCache(maxsize=10_000, ttl=throttle_time)

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:

        message = event.message if isinstance(event, CallbackQuery) else event
        if message.chat.id in self.caches:
            await message.answer(text="Ваш запрос уже обрабатывается")
            return
        else:
            self.caches[message.chat.id] = None
        return await handler(event, data)
