from typing import Any, Awaitable, Callable
from aiogram.types import Message

from aiogram.dispatcher.middlewares.base import BaseMiddleware

from tgbot.models.role import UserRole


class AdminCheckerMiddleware(BaseMiddleware):
    """Check ID for affiliation to admin."""
    def __init__(self, admin_id: int) -> None:
        super().__init__()
        self.admin_id = admin_id


    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]) -> Any:

        if not getattr(event, "from_user", None):
            data["role"] = None
        elif event.from_user.id == self.admin_id:
            data["role"] = UserRole.ADMIN
        else:
            data["role"] = UserRole.USER

        results = await handler(event, data)

        return results





