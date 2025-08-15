from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_menu_keyboard(channel_url: str = ''):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text='🏆 Активные турниры', callback_data='active_tournaments'),
        InlineKeyboardButton(text='✈️ Канал', url=channel_url),
        InlineKeyboardButton(text='💬 Поддержка', callback_data='help'),
        InlineKeyboardButton(text='🧑‍🧑‍🧒‍🧒 О команде', callback_data='about_team'),
    ]

    keyboard.add(*buttons)
    return keyboard
