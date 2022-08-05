from aiogram.dispatcher.fsm.state import State, StatesGroup



class AdminStartMenu(StatesGroup):
    """Start menu."""
    admin_menu = State()




class AdminExerciseMenu(StatesGroup):

    class AddExercise(StatesGroup):
        """Add exercise Group."""
        read_name = State()
        read_description = State()


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
    add_exercise = AddExercise()
    change_exercise = ChangeExercise()
    delete_exercise = DeleteExercise()

