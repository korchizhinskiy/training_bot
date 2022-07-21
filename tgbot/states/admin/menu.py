from aiogram.dispatcher.fsm.state import State, StatesGroup



class AdminStartMenu(StatesGroup):
    """Start menu."""
    admin_menu = State()

