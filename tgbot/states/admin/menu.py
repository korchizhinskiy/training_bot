from aiogram.dispatcher.fsm.state import State, StatesGroup



class AdminStartMenu(StatesGroup):
    """Start menu."""
    admin_menu = State()




class AdminExerciseMenu(StatesGroup):

    class AddExercise(StatesGroup):
        """Add exercise Group."""
        input_name = State()
        input_description = State()


    class ChangeExercise(StatesGroup):
        """Change exercise info Group."""
        parameter_selection = State()
        input_name = State()
        input_description = State()


    """Exercise menu."""
    add_exercise = AddExercise()
    change_exercise = ChangeExercise()

