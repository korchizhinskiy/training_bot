import asyncio
import logging
import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

from tgbot.config import load_config
from tgbot.routes import register_all_routers


logger = logging.getLogger(__name__)

async def connect_to_database(user, password, database, host, echo=False):
    try:
        pool = await asyncpg.create_pool(
                user=user,
                password=password,
                host=host,
                port="5432",
                database=database
                )
        logger.info(f"Подключение к базе данных прошло успешно.")
        return pool
    except Exception:
        logger.info(f"Ошибка при подклчючении к DB")

async def main() -> None:
    """Defaul action for starting bot."""
    logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            )
    config = load_config("config_bot.ini")

    if config.tg_bot.use_redis:
        storage = None
#//     storage = RedisStorage()
    else:
        storage = MemoryStorage()

    pool = await connect_to_database(
            user=config.database.user,
            password=config.database.password,
            database=config.database.database,
            host=config.database.host,
            )

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(storage=storage)

    register_all_routers(dp, config, pool)

    # Start.
    try:
        logger.info("Starting Bot!")
        await dp.start_polling(bot)
    finally:
        await pool.close()
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

