from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.router import Router

from aiogram.types import CallbackQuery, Message
from tgbot.filters.role import Role_Filter
from tgbot.filters.validator import Validator_filter
from tgbot.models.role import UserRole

from tgbot.keyboards.inline_keyboards.admin.menu import Button, get_menu_markup
from tgbot.states.admin.menu import AdminExerciseMenu, AdminStartMenu



admin_menu_router = Router()


@admin_menu_router.message(Role_Filter(user_role=UserRole.ADMIN), Command(commands=["admin"]))
async def admin_welcome(message: Message, state: FSMContext) -> None:
    """Welcome admin in chat and set menu's state."""
    markup = await get_menu_markup([
        [Button(text="Упражнения", callback_data="exercises")], 
        [Button(text="Настройки", callback_data="settings")]
        ])
    await message.answer("Привет, Администратор! Вы успешно прошли авторизацию.", reply_markup=markup)
    await state.set_state(AdminStartMenu.admin_menu)


@admin_menu_router.callback_query(Role_Filter(user_role=UserRole.ADMIN), text="exercises")
async def admin_exercises(call: CallbackQuery, state: FSMContext) -> None:
    """Display exercise's menu in chat"""
    new_markup = await get_menu_markup([
        [Button(text="Добавить", callback_data="add_exercise"), Button(text="Изменить", callback_data="change_exercise")],
        [Button(text="Удалить", callback_data="delete_exercise"), Button(text="Просмотреть все", callback_data="print_exercise")]
        ])
    await call.message.edit_text(text="Пункт управления упражнениями", reply_markup=new_markup)


#<--- Exercises --->
@admin_menu_router.callback_query(Role_Filter(user_role=UserRole.ADMIN), text="add_exercise")
async def admin_add_exercise_input_name(call: CallbackQuery, state: FSMContext) -> None:
    """Get callback from inline button of add exercise."""
    await call.message.edit_text(text="Введите название упражнения.")
    await state.set_state(AdminExerciseMenu.add_exercise.read_name)


@admin_menu_router.message(Role_Filter(user_role=UserRole.ADMIN), Validator_filter(), state=AdminExerciseMenu.add_exercise.read_name)
async def admin_add_exercise_read_name(message: Message, state: FSMContext):
    """Read exercise name, validation and get go next step."""
    exercise_name = message.text.strip().capitalize()
    await state.update_data(exercise_name=exercise_name)
    markup = await get_menu_markup([
        [Button(text="Продолжить", callback_data="input_description"), Button(text="Изменить название", callback_data="add_exercise")],
        [Button(text="Отменить добавление", callback_data="exercises")]
        ])
    await message.answer(f"Вы ввели упражнение:\n {exercise_name}", reply_markup=markup)


@admin_menu_router.message(Role_Filter(user_role=UserRole.ADMIN))
async def admin_input_exercise_name(message: Message, state: FSMContext):
    """Read exercise name and update state's data."""
    await message.answer("Введите описание упражнения.")


@admin_menu_router.message(Role_Filter(user_role=UserRole.ADMIN))
async def admin_input_discription(message: Message, state: FSMContext):
    """Read exercise name and update state's data."""
    state_data = await state.get_data()
    exercise_discription = message.text.strip()
    markup = await get_menu_markup([
        [Button(text="Изменить название", callback_data="add_exercise"), Button(text="Изменить описание", callback_data="exercises")],
        [Button(text="Удалить", callback_data="delete_exercise"), Button(text="Просмотреть все", callback_data="print_exercise")]
        ])
    await message.answer(
            f"Вы вводите упражнение:\n"
            f"Название - {state_data['exercise_name']}\n"
            f"Описание - {exercise_discription}",
            reply_markup=markup
            )
    await state.clear()
    
    
























