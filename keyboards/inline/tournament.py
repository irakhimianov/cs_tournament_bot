from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.back import get_back_button


def get_tournaments(tournaments: dict[int, str]):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = []
    for id, name in tournaments.items():
        buttons.append(
            InlineKeyboardButton(text=name, callback_data=f'get_tournament_{id}'),
        )
    buttons.append(get_back_button('menu'))
    keyboard.add(*buttons)
    return keyboard


def get_tournament_keyboard(tournament_id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text='🔥 Участвовать', callback_data=f'join_tournament_{tournament_id}'),
        get_back_button('active_tournaments'),
    ]
    keyboard.add(*buttons)
    return keyboard
