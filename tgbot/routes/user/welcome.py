from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.filters import Command

from tgbot.filters.role import Role_Filter
from tgbot.models.role import UserRole
from tgbot.states.admin.menu import AdminStartMenu 

from tgbot.services.repository import Repo



user_welcome_router = Router()
# Can use other variants:
# @admin_welcome_router.message(Role_Filter(user_role=[UserRole.ADMIN]), commands=["check"])
# @admin_welcome_router.message(Role_Filter(user_role=[UserRole.ADMIN, UserRole.USER]), commands=["check"])

@user_welcome_router.message(Role_Filter(user_role=UserRole.USER), Command(commands=["start"]))
async def admin_welcome(message: Message, repo: Repo, state: FSMContext) -> None:
    await repo.add_user(message.from_user.id, message.from_user.first_name)
    await message.reply(
            f"Привет, {message.from_user.first_name}"
            )
    await state.set_state(AdminStartMenu.admin_menu)
    

