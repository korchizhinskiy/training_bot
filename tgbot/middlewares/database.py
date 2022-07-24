from typing import Any, Awaitable, Callable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message
from asyncpg import Pool

from tgbot.services.repository import Repo


class DatabaseMiddleware(BaseMiddleware):

    def __init__(self, pool: Pool):
        super().__init__()
        self.pool = pool


    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]
            ) -> Any:
        
        async with self.pool.acquire() as connection:
            async with connection.transaction():

                data["database"] = connection
                data["repo"] = Repo(connection)

                result = await handler(event, data)

                del data["repo"]
                return result
