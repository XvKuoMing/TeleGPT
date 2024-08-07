import logging
from aiohttp import web
from aiogram.utils.chat_action import ChatActionMiddleware
from middlewares.throttling import ThrottlingMiddleware
from aiogram.webhook.aiohttp_server import setup_application

from routers.generator import generator
from config.bot_config import tgpt
from config.dp_config import dp
from config.webhook_config import (set_webhook,
                                   delete_webhook,
                                   webhook_handler,
                                   WEBHOOK_PATH,
                                   SERVER_ADDRESS,
                                   SERVER_PORT
                                   )


def main():

    # include router's middlewares
    generator.message.middleware(ChatActionMiddleware())
    generator.message.middleware(ThrottlingMiddleware())

    # include router's to dispatcher
    dp.include_router(generator)

    # web logic
    app = web.Application()
    dp.startup.register(set_webhook)
    dp.shutdown.register(delete_webhook)
    webhook_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=tgpt)
    web.run_app(app, host=SERVER_ADDRESS, port=SERVER_PORT)


# when using docker compose, logs would be handled by `docker compose logs -f -&> docker.logs &` command
logging.basicConfig(
    # filename="info.log",
    # filemode='a',
    level=logging.INFO
)
main()
