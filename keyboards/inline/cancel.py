from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_cancel_button(callback_data: str = 'cancel', text: str = '❌ Отмена') -> InlineKeyboardButton:
    return InlineKeyboardButton(text=text, callback_data=f'{callback_data}')


def get_cancel_keyboard(callback_data: str = 'cancel', text: str = '❌ Отмена') -> InlineKeyboardMarkup:
    button = get_cancel_button(callback_data=callback_data, text=text)
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(button)
    return keyboard
