from collections import namedtuple
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup 
from aiogram.types.inline_keyboard_button import InlineKeyboardButton



Button = namedtuple("Button", "text callback_data")

# TODO: Remove from admin dir to common dir (../) and use in user/admin routers.
async def get_menu_markup(buttons: list[list[Button]] ) -> InlineKeyboardMarkup:
    """Generate inline murkup by using."""
    keyboard_buttons = []
    for button_row in buttons:
        temp_row = []
        for button in button_row:
            temp_row.append(InlineKeyboardButton(text=button.text, callback_data=button.callback_data))
        keyboard_buttons.append(temp_row)

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    return markup
            








        

