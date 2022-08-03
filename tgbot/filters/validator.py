from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message



class ExerciseValidator(BaseFilter):
    """Filter for role of users."""

    async def __call__(self, message: Message) -> bool:
        if message.text.replace(' ', '').isalpha():
            print("da")
            return True
        else:
            message.answer("Введите корректное название!")
            return False


# TODO: Check admin's authorization for command /admin
class AuthorizationValidator(BaseFilter):
    """Check authorization of admin in bot."""

    async def __call__(self, message: Message) -> bool:
        pass

