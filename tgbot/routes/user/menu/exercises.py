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

from tgbot.misc.callback_data import ExerciseInformationCallbackData, ExercisePaginationCallbackData



exercise_router = Router()
logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        )

#!<--- EXERCISE --->
@exercise_router.message(Role_Filter(user_role=UserRole.USER), Command(commands=["exercises"]), flags={"database_type": "user_repo"})
async def print_exercises(message: Message, repo: UserRepo, state: FSMContext) -> None:
    exercises: tuple = await repo.get_exercises()

    logger.info(f"Количество - {len(exercises)}")
    if (len(exercises)) % 5 == 0:
        max_page = len(exercises)//5 if len(exercises)//5 != 0 else 1
    else:
        max_page = (len(exercises)//5) + 1

    exercise_markup = [[Button(text=exercise, callback_data=exercise)] for exercise in exercises[0:5]]
    navigation_markup = [
             Button(text=f"{1}/{max_page}", callback_data=1),
             Button(text=f"{2} >>", callback_data=ExercisePaginationCallbackData(page_number=2).pack())
             ]

    markup = await get_menu_markup([
        *exercise_markup,
        navigation_markup
        ])
    logger.info(exercise_markup)
    await message.answer("<b>Выберите упражнение</b>", reply_markup=markup)
    await state.update_data(exercises=exercises, max_page=max_page)


@exercise_router.callback_query(Role_Filter(user_role=UserRole.USER), ExercisePaginationCallbackData.filter())
async def check_page_number(call: CallbackQuery, state: FSMContext, callback_data: ExercisePaginationCallbackData) -> None:
    state_data = await state.get_data()
    exercises = state_data['exercises']
    max_page = state_data['max_page']

    current_page = callback_data.page_number

    if current_page == max_page:
        prev_page = current_page - 1
        navigation_markup = [
                 Button(text=f"<< {prev_page}", callback_data=ExercisePaginationCallbackData(page_number=prev_page).pack()),
                 Button(text=f"{current_page}/{max_page}", callback_data=current_page),
                ]
    elif current_page == 1:
        next_page = current_page + 1
        navigation_markup = [
                 Button(text=f"{current_page}/{max_page}", callback_data=current_page),
                 Button(text=f"{next_page} >>", callback_data=ExercisePaginationCallbackData(page_number=next_page).pack())
                ]
    else:
        prev_page = current_page - 1 
        next_page = current_page + 1
        navigation_markup = [
                 Button(text=f"<< {prev_page}", callback_data=ExercisePaginationCallbackData(page_number=prev_page).pack()),
                 Button(text=f"{current_page}/{max_page}", callback_data=current_page),
                 Button(text=f"{next_page} >>", callback_data=ExercisePaginationCallbackData(page_number=next_page).pack())
                ]


    exercise_markup = [[Button(text=exercise, callback_data=exercise)] for exercise in exercises[(current_page-1)*5:current_page*5]]
    
    markup = await get_menu_markup([
        *exercise_markup,
        navigation_markup
        ])
    await call.message.edit_reply_markup(reply_markup=markup)

    
@exercise_router.callback_query(Role_Filter(user_role=UserRole.USER), flags={"database_type": "user_repo"})
async def print_exercise_description(call: CallbackQuery, repo: UserRepo, event_update: Update) -> None:
    exercise_name = event_update.callback_query.data
    exercise_description = await repo.get_exercise_description(exercise_name)
    await call.message.edit_text(f"Описание упражнения:\n\n{exercise_description}")


