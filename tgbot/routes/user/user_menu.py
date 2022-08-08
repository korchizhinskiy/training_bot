import logging
from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.filters import Command

from tgbot.filters.role import Role_Filter
from tgbot.keyboards.inline_keyboards.admin.menu import Button, get_menu_markup
from tgbot.misc.alias import DayOfWeek
from tgbot.misc.callback_data import Chart, MyData
from tgbot.models.role import UserRole

from tgbot.services.repository import Repo, UserRepo



user_menu_router = Router()
logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        )

# Can use other variants:
# @admin_welcome_router.message(Role_Filter(user_role=[UserRole.ADMIN]), commands=["check"])
# @admin_welcome_router.message(Role_Filter(user_role=[UserRole.ADMIN, UserRole.USER]), commands=["check"])

@user_menu_router.message(Role_Filter(user_role=UserRole.USER), Command(commands=["start"]), flags={"database_type": "repo"})
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


@user_menu_router.message(Role_Filter(user_role=UserRole.USER), Command(commands=["exercises"]), flags={"database_type": "user_repo"})
async def print_all_exercises(message: Message, repo: UserRepo) -> None:
    """ Print all exercises. """
    exercises = await repo.print_exercise()
    await message.answer("<b>Весь список упражнений.</b>" + "\n\n⦿ " + "\n⦿ ".join(exercises))


@user_menu_router.message(Role_Filter(user_role=UserRole.USER), Command(commands=["training"]), flags={"database_type": "user_repo"})
async def print_training(message: Message, repo: UserRole, bot) -> None:
    """ Print user's training from database. """
    pass
@user_menu_router.message(Role_Filter(user_role=UserRole.USER), Command(commands=["chart"]), flags={"database_type": "user_repo"})
async def change_chart(message: Message, repo: UserRepo) -> None:
    """ Set/change own chart. """
    if await repo.check_user_chart_week_number(message.from_user.id):
        markup = await get_menu_markup([
            [Button(text="График тренировок", callback_data=MyData(chart=Chart.week_chart).pack())],
            ])
        await message.answer("Изменение графика", reply_markup=markup)
    else:
        pass
        #TODO: Add training into user's database.


@user_menu_router.callback_query(Role_Filter(user_role=UserRole.USER), MyData.filter(), flags={"database_type": "user_repo"})
async def print_training(call: CallbackQuery, repo: UserRepo, callback_data: MyData):
    """ Print user's training from database. """

    if callback_data.chart == Chart.week_chart:
        training_list: str = ''
        weeks_count = await repo.check_user_chart_week_number(call.from_user.id)
        for week in weeks_count:
            training_list += f"Неделя {week}-я:\n"
            days = await repo.check_user_chart_week_day(call.from_user.id, week)
            logger.info(f"{days = }")
            for day in days:
                day_name = DayOfWeek.get_value(day)
                training_list += f"День недели - {day_name}\n"
                exercises = await repo.check_user_chart_exercises(call.from_user.id, week, day)
                for exercise in exercises:
                    training_list += f"Упражнение {exercise[0][3]}\n{exercise[0][0]}\nПодходы: {exercise[0][1]}\nПовторения: {exercise[0][2]}\n"
        await call.message.answer(training_list)

