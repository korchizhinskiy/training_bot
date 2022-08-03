from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.router import Router

from aiogram.types import CallbackQuery, Message
from tgbot.filters.role import Role_Filter
from tgbot.filters.validator import ExerciseValidator
from tgbot.models.role import UserRole

from tgbot.keyboards.inline_keyboards.admin.menu import Button, get_menu_markup
from tgbot.states.admin.menu import AdminExerciseMenu


admin_menu_router = Router()

# TODO: Delete inline buttons, when go to next step.
@admin_menu_router.message(Role_Filter(user_role=UserRole.ADMIN), Command(commands=["admin"]))
async def admin_welcome(message: Message) -> None:
    """Welcome admin in chat and set menu's state."""
    markup = await get_menu_markup([
        [Button(text="Авторизоваться", callback_data="menu")]])
    await message.answer("Привет, Администратор! Нажми на кнопку, чтобы пройти авторизацию.", reply_markup=markup)


@admin_menu_router.callback_query(Role_Filter(user_role=UserRole.ADMIN), text="menu")
async def admin_menu(call: CallbackQuery) -> None:
    markup = await get_menu_markup([
        [Button(text="Упражнения", callback_data="exercises")], 
        [Button(text="Настройки", callback_data="settings")]
        ])
    await call.message.edit_text("<b>Меню администратора</b>", reply_markup=markup)


@admin_menu_router.callback_query(Role_Filter(user_role=UserRole.ADMIN), text="exercises")
async def admin_exercises(call: CallbackQuery, state: FSMContext) -> None:
    """Display exercise's menu in chat"""
    new_markup = await get_menu_markup([
        [Button(text="Добавить", callback_data="add_exercise"), Button(text="Изменить", callback_data="change_exercise")],
        [Button(text="Удалить", callback_data="delete_exercise"), Button(text="Просмотреть все", callback_data="print_exercise")]
        ])
    await call.message.edit_text(text="Пункт управления упражнениями", reply_markup=new_markup)


#!<--- Exercises --->
#! <--- Add exercise --->
@admin_menu_router.callback_query(Role_Filter(user_role=UserRole.ADMIN), text="add_exercise")
async def admin_add_exercise_input_name(call: CallbackQuery, state: FSMContext) -> None:
    """Get callback from inline button of add exercise."""
    await call.message.edit_text(text="Введите название упражнения.")
    await state.set_state(AdminExerciseMenu.add_exercise.read_name)


@admin_menu_router.message(Role_Filter(user_role=UserRole.ADMIN), ExerciseValidator(), state=AdminExerciseMenu.add_exercise.read_name)
async def admin_add_exercise_read_name(message: Message, state: FSMContext):
    """Read exercise name, validation and get go next step."""
    exercise_name = message.text.strip().capitalize()
    await state.update_data(exercise_name=exercise_name)
    markup = await get_menu_markup([
        [Button(text="Продолжить", callback_data="input_description"), Button(text="Изменить название", callback_data="add_exercise")],
        [Button(text="Отменить добавление", callback_data="exercises")]
        ])
    await message.answer(f"Вы ввели упражнение:\n<b>{exercise_name}</b>", reply_markup=markup)
    await state.set_state('*')


@admin_menu_router.callback_query(Role_Filter(user_role=UserRole.ADMIN), text="input_description")
async def admin_input_exercise_name(call: CallbackQuery, state: FSMContext):
    """Read exercise name and update state's data."""
    await call.message.delete()
    await call.message.answer("Введите описание упражнения.")
    await state.set_state(AdminExerciseMenu.add_exercise.read_description)


@admin_menu_router.message(Role_Filter(user_role=UserRole.ADMIN), state=AdminExerciseMenu.add_exercise.read_description)
async def admin_input_discription(message: Message, state: FSMContext):
    """Read exercise name and update state's data."""
    state_data = await state.get_data()
    exercise_discription = message.text.strip()
    markup = await get_menu_markup([
        [Button(text="Подтвердить", callback_data="output_result")],
        [Button(text="Изменить описание", callback_data="input_description"), Button(text="Удалить", callback_data="menu")]
        ])
    await message.answer(
            f"Подтвердите добавление упражнения\n"
            f"Название - {state_data['exercise_name']}\n"
            f"Описание - {exercise_discription}",
            reply_markup=markup
           )
    await state.clear()

@admin_menu_router.callback_query(Role_Filter(user_role=UserRole.ADMIN), text="output_result")
async def print_result(call: CallbackQuery, state: FSMContext):
    """Print result of exercise and add to database."""
    markup = await get_menu_markup([
        [Button(text="Добавить упражнение ещё", callback_data="add_exercise"), Button(text="Вернуться в меню", callback_data="menu")]
        ])
    await call.message.edit_text("Вы успешно добавили упражнение.", reply_markup=markup)
    await state.clear()
    

@admin_menu_router.message(Role_Filter(user_role=UserRole.ADMIN))
async def delete_false_message(message: Message):
    await message.delete()


