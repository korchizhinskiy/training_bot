from typing import Any, Awaitable, Callable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.dispatcher.flags.getter import get_flag
from aiogram.types import Message
from asyncpg import Pool

from tgbot.services.repository import AdminRepo, Repo, UserRepo


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
        
        async with self.pool.acquire() as connection: # AttributeError TODO
            async with connection.transaction():

                data["database"] = connection
                database_type = get_flag(data, "database_type")
                if database_type:
                    match database_type:
                        case "repo":
                            data["repo"] = Repo(connection)
                        case "admin_repo":
                            data["repo"] = AdminRepo(connection)
                        case "user_repo":
                            data["repo"] = UserRepo(connection)
                else:
                    data["repo"] = None
                        
                result = await handler(event, data)

                del data["repo"]
                return result
