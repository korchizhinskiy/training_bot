from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.router import Router

from aiogram.types import CallbackQuery, Message
from tgbot.filters.role import Role_Filter
from tgbot.models.role import UserRole

from tgbot.keyboards.inline_keyboards.admin.menu import Button, get_menu_markup
from tgbot.states.admin.menu import AdminStartMenu



admin_menu_router = Router()


@admin_menu_router.message(Role_Filter(user_role=UserRole.ADMIN), Command(commands=["admin"]))
async def admin_welcome(message: Message, state: FSMContext) -> None:
    """Welcome admin in chat and set menu's state."""
    markup = get_menu_markup([
        [Button(text="Упражнения", callback_data="exercises")], 
        [Button(text="Настройки", callback_data="settings")]
        ])
    await message.answer("Привет, Администратор! Вы успешно прошли авторизацию.", reply_markup=markup)
    await state.set_state(AdminStartMenu.admin_menu)


@admin_menu_router.callback_query(Role_Filter(user_role=UserRole.ADMIN), text="exercises", state=AdminStartMenu.admin_menu)
async def admin_exercises(call: CallbackQuery, state: FSMContext) -> None:
    """Display exercise's menu in chat"""
    new_markup = get_menu_markup([
        [Button(text="Добавить", callback_data="add_exercise"), Button(text="Изменить", callback_data="change_exercise")],
        [Button(text="Удалить", callback_data="delete_exercise"), Button(text="Просмотреть все", callback_data="print_exercise")]
        ])
    await call.message.edit_text(text="Пункт управления упражнениями", reply_markup=new_markup)
