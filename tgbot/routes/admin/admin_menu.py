from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.router import Router

from aiogram.types import Message

from tgbot.keyboards.inline_keyboards.admin.menu import Button, get_menu_markup
from tgbot.states.admin.menu import AdminStartMenu



admin_menu_router = Router()


@admin_menu_router.message(Command(commands=["admin"]))
async def admin_welcome(message: Message, state: FSMContext) -> None:
    markup = get_menu_markup([
        [Button(text="Привет", callback_data="Приветствие"), Button(text="Пока", callback_data="Прощание")]
        ])
    await message.reply("Привет, Администратор! Вы успешно прошли авторизацию.", reply_markup=markup)
    await state.set_state(AdminStartMenu.admin_menu)
