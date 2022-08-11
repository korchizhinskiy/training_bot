import logging
from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.filters import Command
from magic_filter import F

from tgbot.filters.role import Role_Filter
from tgbot.keyboards.inline_keyboards.admin.menu import Button, get_menu_markup
from tgbot.misc.alias import DayOfWeek
from tgbot.misc.callback_data import ChartCallbackData
from tgbot.models.role import UserRole

from tgbot.services.repository import UserRepo
from tgbot.states.user.menu import UserTrainingMenu



chart_router = Router()
logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        )

#!<--- CHART --->
@chart_router.message(Role_Filter(user_role=UserRole.USER), Command(commands=["chart"]), flags={"database_type": "user_repo"})
async def change_chart(message: Message, repo: UserRepo, state: FSMContext) -> None:
    """ Set/change own chart. """
    if await repo.check_user_chart_week_number(message.from_user.id):
        markup = await get_menu_markup([
            [Button(text="График тренировок", callback_data=ChartCallbackData(chart="training_chart").pack())],
            [Button(text="Добавление тренировочного дня", callback_data=ChartCallbackData(chart="add_training_day").pack())],
            [Button(text="Удаление тренировочного дня", callback_data=ChartCallbackData(chart="delete_training_day").pack())]
            ])
        await message.answer("Изменение графика", reply_markup=markup)
    else:
        markup = await get_menu_markup([
            [Button(text="Добавление тренировочного дня", callback_data=ChartCallbackData(chart="add_training_day").pack())]
            ])
        await message.answer("Изменение графика", reply_markup=markup)

    await state.set_state(UserTrainingMenu.choice_of_changing)


@chart_router.callback_query(Role_Filter(user_role=UserRole.USER), ChartCallbackData.filter(), 
                                 state=UserTrainingMenu.choice_of_changing, flags={"database_type": "user_repo"})
async def choice_of_changin_chart(call: CallbackQuery, repo: UserRepo, callback_data: ChartCallbackData, state: FSMContext) -> None:
    """ Print user's training from database. """
    if callback_data.chart == "training_chart":
        training_list: str = ''
        tabulation = "\t"*4
        weeks_count = await repo.check_user_chart_week_number(call.from_user.id)
        for week in weeks_count:
            training_list += f"\n<u><b>Неделя {week}-я:</b></u>\n"
            days = await repo.check_user_chart_week_day(call.from_user.id, week)
            logger.info(f"{days = }")
            for day in days:
                day_name = DayOfWeek.get_value(day)
                training_list += f"{tabulation}<u><b>День недели - {day_name}</b></u>\n"
                exercises = await repo.check_user_chart_exercises(call.from_user.id, week, day)
                for exercise in exercises:
                    training_list += f"{tabulation}{exercise[0][0]} --- Подходы - {exercise[0][1]} --- Повторения - {exercise[0][2]}\n"
        await call.message.edit_text(training_list)
        await state.clear()


    elif callback_data.chart == "add_training_day":
        weeks = await repo.check_user_chart_week_number(call.from_user.id)
        week_markup = [[Button(text=f"{week}-я неделя", callback_data=ChartCallbackData(chart=f"{week}_week").pack())] for week in weeks]
        markup = await get_menu_markup([
            [Button(text=f"Альтернативная неделя", callback_data=ChartCallbackData(chart=f"add_week").pack())],
            *week_markup
            ])
        await call.message.edit_text("Выберите неделю для добавления", reply_markup=markup)
        await state.set_state(UserTrainingMenu.add_training_day.choice_of_week)

    elif callback_data.chart == "delete_training_day":
        weeks = await repo.check_user_chart_week_number(call.from_user.id)
        markup = await get_menu_markup([
            [Button(text=f"{week}-я неделя", callback_data=ChartCallbackData(chart=f"{week}_week").pack())] for week in weeks
            ])
        await call.message.edit_text("Выберите неделю для удаления тренировочного дня", reply_markup=markup)
        await state.set_state(UserTrainingMenu.delete_training_day.choice_of_week)

        

@chart_router.callback_query(Role_Filter(user_role=UserRole.USER), ChartCallbackData.filter(F.chart.split('_')[1] == "week"), 
                                 state=UserTrainingMenu.add_training_day.choice_of_week, flags={"database_type": "user_repo"})
async def add_chart_day(call: CallbackQuery, repo: UserRepo, callback_data: ChartCallbackData, state: FSMContext) -> None:
    if callback_data.chart.split('_')[0] == "add":
        week_number = await repo.get_maximum_week_number(call.from_user.id) + 1
    else:
        week_number = int(callback_data.chart.split('_')[0]) #// Get number of week.

    await state.update_data(week_number=week_number)
    days = await repo.check_user_chart_week_day(call.from_user.id, week_number)
    unused_days = set(days).symmetric_difference({1, 2, 3, 4, 5, 6, 7})
    markup = await get_menu_markup([
       [Button(text=f"{DayOfWeek.get_value(day)}", callback_data=ChartCallbackData(chart=f"{day}_day").pack())] for day in unused_days 
        ])
    await call.message.edit_text("Выберите день недели", reply_markup=markup)
    await state.set_state(UserTrainingMenu.add_training_day.choice_of_day)


@chart_router.callback_query(Role_Filter(user_role=UserRole.USER), ChartCallbackData.filter(F.chart.split('_')[1] == "day"), 
                                 state=UserTrainingMenu.add_training_day.choice_of_day, flags={"database_type": "user_repo"})
async def result_of_add_day(call: CallbackQuery, repo: UserRepo, callback_data: ChartCallbackData, state: FSMContext) -> None:
    week_day = int(callback_data.chart.split('_')[0])
    state_data = await state.get_data()
    await call.message.edit_text(f"День недели {DayOfWeek.get_value(week_day)} добавлен в неделю № {state_data['week_number']}")
    await repo.add_training_day(call.from_user.id, state_data['week_number'], week_day)


@chart_router.callback_query(Role_Filter(user_role=UserRole.USER), ChartCallbackData.filter(F.chart.split('_')[1] == "week"), 
                                 state=UserTrainingMenu.delete_training_day.choice_of_week, flags={"database_type": "user_repo"})
async def delete_chart_day(call: CallbackQuery, repo: UserRepo, callback_data: ChartCallbackData, state: FSMContext) -> None:
    week_number = int(callback_data.chart.split('_')[0]) #// Get number of week.
    await state.update_data(week_number=week_number)
    days = await repo.check_user_chart_week_day(call.from_user.id, week_number)
    markup = await get_menu_markup([
       [Button(text=f"{DayOfWeek.get_value(day)}", callback_data=ChartCallbackData(chart=f"{day}_day").pack())] for day in days
        ])
    await call.message.edit_text("Выберите день недели", reply_markup=markup)
    await state.set_state(UserTrainingMenu.delete_training_day.choice_of_day)


@chart_router.callback_query(Role_Filter(user_role=UserRole.USER), ChartCallbackData.filter(F.chart.split('_')[1] == "day"), 
                                 state=UserTrainingMenu.delete_training_day.choice_of_day, flags={"database_type": "user_repo"})
async def result_of_delete_day(call: CallbackQuery, repo: UserRepo, callback_data: ChartCallbackData, state: FSMContext) -> None:
    week_day = int(callback_data.chart.split('_')[0])
    state_data = await state.get_data()
    await call.message.edit_text(f"День недели {DayOfWeek.get_value(week_day)} удален из недели № {state_data['week_number']}")
    await repo.delete_training_day(call.from_user.id, state_data['week_number'], week_day)
