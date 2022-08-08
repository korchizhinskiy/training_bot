from enum import Enum
from aiogram.dispatcher.filters.callback_data import CallbackData


class Chart(Enum):
    week_chart = "print_week_chart"

    
class MyData(CallbackData, prefix="my_data"):
    chart: Chart
