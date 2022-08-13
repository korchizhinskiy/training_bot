
import logging
from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.filters import Command

from tgbot.filters.role import Role_Filter
from tgbot.keyboards.inline_keyboards.admin.menu import Button, get_menu_markup
from tgbot.misc.alias import DayOfWeek
from tgbot.misc.callback_data import ExerciseCallbackData
from tgbot.models.role import UserRole

from tgbot.services.repository import Repo, UserRepo
from tgbot.states.user.menu import UserTrainingMenu



training_router = Router()
logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        )

# Can use other variants:
# @admin_welcome_router.message(Role_Filter(user_role=[UserRole.ADMIN]), commands=["check"])
# @admin_welcome_router.message(Role_Filter(user_role=[UserRole.ADMIN, UserRole.USER]), commands=["check"])

@training_router.message(Role_Filter(user_role=UserRole.USER), Command(commands=["start"]), flags={"database_type": "repo"})
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


#!<--- TRAINING --->
@training_router.message(Role_Filter(user_role=UserRole.USER), Command(commands=["training"]), flags={"database_type": "user_repo"})
async def change_training_day(message: Message, repo: UserRole, state: FSMContext) -> None:
    """ Print user's training from database. """
    markup = await get_menu_markup([
        [Button(text="Удалить упражнение из тренировочного дня", callback_data=ExerciseCallbackData(training="delete_exercise_from_training_day").pack())],
        [Button(text="Добавить упражнение в тренировочный день", callback_data=ExerciseCallbackData(training="add_exercise_to_training_day").pack())],
        ])
    await message.answer("Пункт управления тренировками", reply_markup=markup)
    await state.set_state(UserTrainingMenu.choice_of_changing)


@training_router.callback_query(Role_Filter(user_role=UserRole.USER), ExerciseCallbackData.filter(), state=UserTrainingMenu.choice_of_changing,
                                 flags={"database_type": "user_repo"})
async def choice_of_change_week(call: CallbackQuery, repo: UserRepo, callback_data: ExerciseCallbackData, state: FSMContext) -> None:
    """ Answer for callback query of change training days. """
    if callback_data.training == "delete_exercise_from_training_day":
        await call.answer("Выбрал удаление")

    elif callback_data.training == "add_exercise_to_training_day":
        weeks = await repo.check_user_chart_week_number(call.from_user.id)
        markup = await get_menu_markup([
            [Button(text=f"{week}-я неделя", callback_data=ExerciseCallbackData(training=f"{week}_week").pack())] for week in weeks
            ])
        await call.message.edit_text("Выберите неделю, которую хотите поменять.", reply_markup=markup)
        await state.set_state(UserTrainingMenu.add_exercise.read_week)


@training_router.callback_query(Role_Filter(user_role=UserRole.USER), ExerciseCallbackData.filter(), 
        state=UserTrainingMenu.add_exercise.read_week, flags={"database_type": "user_repo"})
async def choice_of_change_day(call: CallbackQuery, repo: UserRepo, callback_data: ExerciseCallbackData, state: FSMContext) -> None:
    """ Ask about days of changing. """
    #// Get number of day.
    week = callback_data.training.split('_')[0]
    await state.update_data(week=int(week))
    days = await repo.check_user_chart_week_day(call.from_user.id, int(week))
    markup = await get_menu_markup([
        [Button(text=f"{DayOfWeek.get_value(int(day))}", callback_data=ExerciseCallbackData(training=f"{int(day)}").pack())] for day in days
        ])
    await call.message.edit_text("Выберите день недели", reply_markup=markup)
    await state.set_state(UserTrainingMenu.add_exercise.read_day)


@training_router.callback_query(Role_Filter(user_role=UserRole.USER), ExerciseCallbackData.filter(), 
                                 state=UserTrainingMenu.add_exercise.read_day)
async def ask_exercise_name(call: CallbackQuery, callback_data: ExerciseCallbackData, state: FSMContext) -> None:
    """ Ask about days of changing. """
    #// Get number of day.
    day = callback_data.training
    await state.update_data(day=day)
    await call.message.edit_text("Введите название упражнения")
    await state.set_state(UserTrainingMenu.add_exercise.read_exercise_name)


@training_router.message(Role_Filter(user_role=UserRole.USER), state=UserTrainingMenu.add_exercise.read_exercise_name)
async def ask_exercise_count_approaches(message: Message, state: FSMContext) -> None:
    exercise_name = message.text.strip().capitalize()
    await state.update_data(exercise_name=exercise_name)
    await message.answer("Введите количество подходов")
    await state.set_state(UserTrainingMenu.add_exercise.read_count_approaches)


@training_router.message(Role_Filter(user_role=UserRole.USER), state=UserTrainingMenu.add_exercise.read_count_approaches)
async def ask_exercise_count_repetition(message: Message, state: FSMContext) -> None:
    exercise_count_approaches = message.text.strip()
    await state.update_data(exercise_count_approaches=exercise_count_approaches)
    await message.answer("Введите количество повторений")
    await state.set_state(UserTrainingMenu.add_exercise.read_count_repetition)

#TODO: Add ordering
@training_router.message(Role_Filter(user_role=UserRole.USER), state=UserTrainingMenu.add_exercise.read_count_repetition, flags={"database_type": "user_repo"})
async def output_result_of_add_exercise(message: Message, state: FSMContext, repo: UserRepo) -> None:
    exercise_count_repetition = message.text.strip()
    state_data = await state.get_data()
    await message.answer(f"Вы ввели упражнение {state_data['exercise_name']}\n"
                         f"Количество подходов - {state_data['exercise_count_approaches']}\n"
                         f"Количество повторений - {exercise_count_repetition}")
    await repo.add_exercise_into_training_day(message.from_user.id, state_data['week'], state_data['day'], state_data['exercise_name'],
                                              state_data['exercise_count_approaches'], exercise_count_repetition)
    await state.clear()

