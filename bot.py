import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

from tgbot.config import load_config
from tgbot.routes import register_all_routers



logger = logging.getLogger(__name__)



def create_pool(user, password, database, host, echo=False):
    # TODO check your db connector
    pass


async def main() -> None:
    """Defaul action for starting bot."""
    logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            )
    config = load_config("config_bot.ini")

    if config.tg_bot.use_redis:
        storage = MemoryStorage()
#       storage = RedisStorage()
    else:
        storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=storage)

    register_all_routers(dp, config)

    # Start.
    try:
        logger.info("Starting Bot!")
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


def cli():
    """Wrapper for command line."""
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")


if __name__ == "__main__":
    cli()

