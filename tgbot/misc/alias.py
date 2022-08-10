from enum import Enum


class DayOfWeek(Enum):

    MONDAY = (1, "Понедельник")
    TUESDAY = (2, "Вторник")
    WEDNESDAY = (3, "Среда")
    THURSDAY = (4, "Четверг")
    FRIDAY = (5, "Пятница")
    SATURDAY = (6, "Суббота")
    SUNDAY = (7, "Воскресенье")


    @classmethod
    def get_value(cls, number: int | str) -> str:
        """ Get string - day of week. """
        for day in cls:
            if day.value[0] == int(number):
                return day.value[1]
        else:
            raise ValueError("Вы вводите числа меньше 1 или больше 9.")

