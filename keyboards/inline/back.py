from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_back_button(callback_data: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text='◀ Назад', callback_data=callback_data)


def get_back_keyboard(callback_data: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(get_back_button(callback_data=callback_data))
    return keyboard
