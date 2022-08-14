import logging
from aiogram import Router
from aiogram.types import CallbackQuery, Message, Update
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.filters import Command

from tgbot.filters.role import Role_Filter
from tgbot.keyboards.inline_keyboards.admin.menu import Button, get_menu_markup
from tgbot.models.role import UserRole

from tgbot.services.repository import UserRepo
from tgbot.states.user.menu import UserTrainingMenu

from tgbot.misc.callback_data import ExercisePaginationCallbackData
from tgbot.misc.pagination import get_pagination



exercise_router = Router()
logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        )

#!<--- EXERCISE --->

@exercise_router.message(Role_Filter(user_role=UserRole.USER), Command(commands=["exercises"]), flags={"database_type": "user_repo"})
async def print_exercises(message: Message, repo: UserRepo, state: FSMContext) -> None:
    markup = await get_pagination(repo, state, callback_data=ExercisePaginationCallbackData(page_number=1))
    await message.answer("Выберите упражнение", reply_markup=markup)


@exercise_router.callback_query(Role_Filter(user_role=UserRole.USER), ExercisePaginationCallbackData.filter())
async def check_page_number(call: CallbackQuery, state: FSMContext, callback_data: ExercisePaginationCallbackData, repo: UserRepo) -> None:
    markup = await get_pagination(repo, state, callback_data)
    await call.message.edit_text("Выберите упражнение", reply_markup=markup)

    
@exercise_router.callback_query(Role_Filter(user_role=UserRole.USER), flags={"database_type": "user_repo"})
async def print_exercise_description(call: CallbackQuery, repo: UserRepo, event_update: Update) -> None:
    exercise_name = event_update.callback_query.data
    exercise_description = await repo.get_exercise_description(exercise_name)
    await call.message.edit_text(f"Описание упражнения:\n\n{exercise_description}")


