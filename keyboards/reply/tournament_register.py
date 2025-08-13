from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_contact_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton(text='Отправить', request_contact=True)
    keyboard.add(button)
    return keyboard
