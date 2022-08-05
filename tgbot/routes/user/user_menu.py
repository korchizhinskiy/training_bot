from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.filters import Command

from tgbot.filters.role import Role_Filter
from tgbot.models.role import UserRole

from tgbot.services.repository import Repo, UserRepo



user_menu_router = Router()
# Can use other variants:
# @admin_welcome_router.message(Role_Filter(user_role=[UserRole.ADMIN]), commands=["check"])
# @admin_welcome_router.message(Role_Filter(user_role=[UserRole.ADMIN, UserRole.USER]), commands=["check"])

@user_menu_router.message(Role_Filter(user_role=UserRole.USER), Command(commands=["start"]), flags={"database_type": "repo"})
async def admin_welcome(message: Message, repo: Repo) -> None:
    if await repo.add_user(message.from_user.id, message.from_user.first_name):
        await message.answer(
                f"Привет, {message.from_user.first_name}. Давай знакомиться!👋\n"
                f"Я твой личный тренер, буду помогать тебе становиться лучше.\n"
                f"Надеюсь, что ты уже определился с целями 💪\n"
                f"Чтобы управлять мной, ты можешь воспользоваться пунктом \"Меню\" в нижней части экрана.\n"
                f"Удачи тебе, а я помогу тебе достигнуть желаемых результатов!😎"
                )
    else:
        await message.answer(f"{message.from_user.first_name.capitalize()}, привет. Снова рад встрече. Помнишь, как мною пользоваться? 👽 ")


@user_menu_router.message(Role_Filter(user_role=UserRole.USER), Command(commands=["exercises"]), flags={"database_type": "user_repo"})
async def admin_welcome(message: Message, repo: UserRepo) -> None:
    exercises = await repo.print_exercise()
    await message.answer("<b>Весь список упражнений.</b>" + "\n\n⦿ " + "\n⦿ ".join(exercises))

    

