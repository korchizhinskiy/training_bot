from aiogram.dispatcher.fsm.state import State, StatesGroup



class UserTrainingMenu(StatesGroup):

    class AddExerciseInTrainingDay(StatesGroup):
        """Add exercise Group."""
        read_week = State()
        read_day = State()
        read_exercise_name = State()
        read_count_approaches = State()
        read_count_repetition = State()


    class DeleteExerciseFromTrainingDay(StatesGroup):
        """Delete exercise Group."""
        read_week = State()
        read_day = State()
        read_exercise_name = State()


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



    choice_of_changing = State()
    add_exercise = AddExerciseInTrainingDay()
    delete_exercise = DeleteExerciseFromTrainingDay()
    add_training_day = AddTrainingDay()
    delete_training_day = DeleteTrainingDay()


