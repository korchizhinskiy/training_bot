from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup 
from tgbot.keyboards.inline_keyboards.admin.menu import Button, get_menu_markup
from tgbot.misc.callback_data import ExercisePaginationCallbackData
from tgbot.services.repository import UserRepo


async def get_pagination(repo: UserRepo, state: FSMContext, callback_data: ExercisePaginationCallbackData) -> InlineKeyboardMarkup:
    state_data = await state.get_data()

    #// Exercise list.
    if state_data.get('exercises'):
        exercises = state_data['exercises']
    else:
        exercises: tuple = await repo.get_exercises()
        await state.update_data(exercises=exercises)

    # // Max page.
    if state_data.get('max_page'):
        max_page = state_data['max_page']
        await state.update_data(max_page=max_page)
    else:
        if (len(exercises)) % 5 == 0:
            max_page = len(exercises)//5 if len(exercises)//5 != 0 else 1
        else:
            max_page = (len(exercises)//5) + 1

    #// Set current page.
    if callback_data.page_number:
       current_page = callback_data.page_number
    else:
        current_page = 1

    # // Correct output of listing.
    if current_page == max_page:
        prev_page = current_page - 1
        navigation_markup = [
                 Button(text=f"<< {prev_page}", callback_data=ExercisePaginationCallbackData(page_number=prev_page).pack()),
                 Button(text=f"{current_page}/{max_page}", callback_data=current_page),
                ]
    elif current_page == 1:
        next_page = current_page + 1
        navigation_markup = [
                 Button(text=f"{current_page}/{max_page}", callback_data=current_page),
                 Button(text=f"{next_page} >>", callback_data=ExercisePaginationCallbackData(page_number=next_page).pack())
                ]
    else:
        prev_page = current_page - 1 
        next_page = current_page + 1
        navigation_markup = [
                 Button(text=f"<< {prev_page}", callback_data=ExercisePaginationCallbackData(page_number=prev_page).pack()),
                 Button(text=f"{current_page}/{max_page}", callback_data=current_page),
                 Button(text=f"{next_page} >>", callback_data=ExercisePaginationCallbackData(page_number=next_page).pack())
                ]


    exercise_markup = [[Button(text=exercise, callback_data=exercise)] for exercise in exercises[(current_page-1)*5:current_page*5]]
    
    markup = await get_menu_markup([
        *exercise_markup,
        navigation_markup
        ])

    return markup
