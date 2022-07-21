from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.fsm.storage.base import StateType
from aiogram.dispatcher.fsm.context import FSMContext

from tgbot.filters.role import Role_Filter
from tgbot.models.role import UserRole

from tgbot.states.admin.menu import AdminStartMenu


admin_welcome_router = Router()

# Can use other variants:
# @admin_welcome_router.message(Role_Filter(user_role=[UserRole.ADMIN]), commands=["check"])
# @admin_welcome_router.message(Role_Filter(user_role=[UserRole.ADMIN, UserRole.USER]), commands=["check"])
@admin_welcome_router.message(Role_Filter(user_role=UserRole.ADMIN), commands=["admin"])
async def admin_welcome(message: Message, state: FSMContext) -> None:
    await message.reply("Привет, Администратор! Вы успешно прошли авторизацию.")
    await state.set_state(AdminStartMenu.admin_menu)

