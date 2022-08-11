from aiogram.dispatcher.fsm.state import State, StatesGroup



class UserTrainingMenu(StatesGroup):

    class AddExercise(StatesGroup):
        """Add exercise Group."""
        read_week = State()
        read_day = State()
        read_exercise_name = State()
        read_count_approaches = State()
        read_count_repetition = State()


    class AddTrainingDay(StatesGroup):
        """Add training day Group."""
        choice_of_week = State()
        choice_of_day = State()


    class DeleteTrainingDay(StatesGroup):
        """Add training day Group."""
        choice_of_week = State()
        choice_of_day = State()


    class ChangeExercise(StatesGroup):
        """Change exercise info Group."""
        select_exercise = State()
        read_name = State()
        read_description = State()


    class DeleteExercise(StatesGroup):
        """Change exercise info Group."""
        read_name = State()


    """Exercise menu."""
    exercise_menu = State()
    choice_of_changing = State()
    add_exercise = AddExercise()
    add_training_day = AddTrainingDay()
    delete_training_day = DeleteTrainingDay()
    change_exercise = ChangeExercise()
    delete_exercise = DeleteExercise()


