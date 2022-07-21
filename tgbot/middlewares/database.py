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

        data["database"] = await self.pool.acquire()
        data["repo"] = Repo(self.pool)

        result = await handler(event, data)

        del data["repo"]
        if data["database"]:
            await self.pool.release(data["database"])
        return result
