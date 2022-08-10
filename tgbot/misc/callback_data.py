from enum import Enum
from aiogram.dispatcher.filters.callback_data import CallbackData


class Training(Enum):
    delete_exercise_from_day = "delete_exercise_from_day"
    add_exercise_to_day = "add_exercise_to_day"

    
class MyCallbackData(CallbackData, prefix="my_data"):
    training: str
